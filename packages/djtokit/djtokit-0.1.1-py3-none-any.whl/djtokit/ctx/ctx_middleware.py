# db_read_after_write.py
from . import context


class CtxMiddleware:
    """
    绑定ctx到请求上下文
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 设置新的上下文信息
        # user_id 和 request_id 需要根据你的项目实际情况设置
        context.RequestContext.set_context(user_id=request.user.id, request_id=request.id)

        response = self.get_response(request)

        # 请求处理完毕，重置上下文
        context.RequestContext.reset()
        return response
