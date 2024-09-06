import threading
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class RequestContextData:
    """
    请求上下 ctx
    """
    user_id: Optional[int] = None
    request_id: Optional[str] = None
    orm_write: Optional[str] = None
    using: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


_context_var: ContextVar[Optional[RequestContextData]] = ContextVar('_context_var', default=None)


class RequestContext:
    """
    请求上下中间件使用
    """
    @staticmethod
    def set_context(user_id: Optional[int] = None, request_id: Optional[str] = None, **kwargs):
        _context_var.set(RequestContextData(user_id=user_id, request_id=request_id, extra=kwargs))

    @staticmethod
    def get_context() -> Optional[RequestContextData]:
        return _context_var.get()

    @staticmethod
    def reset():
        _context_var.set(None)

    @staticmethod
    def update_context(**kwargs):
        """
        kwargs:
        """
        current_context = _context_var.get()
        if not current_context:
            return None
        # extra 会增量
        if 'extra' in kwargs:
            extra = kwargs.pop('extra')
            current_context.extra.update(extra)
        for key, value in kwargs.items():
            if hasattr(current_context, key):
                setattr(current_context, key, value)
        _context_var.set(current_context)
        return


def thread_function(user_id):
    # Set context for this thread
    tid = threading.current_thread().ident
    RequestContext.set_context(user_id=tid, request_id=f'---{tid}',)
    # Simulate doing some work and retrieving the context
    context = RequestContext.get_context()
    print(f"Thread {threading.current_thread().name}: {context}\n")
    return


def main():
    # Create threads
    threads = [threading.Thread(target=thread_function, args=(i,)) for i in range(5)]
    # Start threads
    for thread in threads:
        thread.start()
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    return


if __name__ == '__main__':
    main()
