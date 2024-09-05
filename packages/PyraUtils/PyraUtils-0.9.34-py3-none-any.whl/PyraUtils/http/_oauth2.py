from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc6749.errors import OAuth2Error

class OAuth2ClientError(Exception):
    """Custom exception class for OAuth2Client errors"""
    pass

class OAuth2Client:
    def __init__(self, client_id, client_secret, authorize_url, token_url, redirect_uri, scope):
        """
        初始化OAuth2Client实例。

        :param client_id: OAuth2 客户端ID
        :param client_secret: OAuth2 客户端密钥
        :param authorize_url: 授权URL
        :param token_url: 令牌URL
        :param redirect_uri: 重定向URI
        :param scope: 授权范围
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorize_url = authorize_url
        self.token_url = token_url
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.session = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri, scope=scope)

    def get_authorization_url(self):
        """
        获取授权URL。

        :return: 授权URL和状态
        :raises OAuth2ClientError: 如果获取授权URL失败
        """
        try:
            uri, state = self.session.create_authorization_url(self.authorize_url)
            return uri, state
        except OAuth2Error as e:
            raise OAuth2ClientError(f"Error obtaining authorization URL: {e}")

    def fetch_token(self, authorization_response):
        """
        使用授权响应获取访问令牌。

        :param authorization_response: 授权响应URL
        :return: 访问令牌
        :raises OAuth2ClientError: 如果获取访问令牌失败
        """
        try:
            token = self.session.fetch_token(self.token_url, authorization_response=authorization_response)
            return token
        except OAuth2Error as e:
            raise OAuth2ClientError(f"Error fetching token: {e}")

    def refresh_token(self, refresh_token):
        """
        使用刷新令牌获取新的访问令牌。

        :param refresh_token: 刷新令牌
        :return: 新的访问令牌
        :raises OAuth2ClientError: 如果刷新访问令牌失败
        """
        try:
            new_token = self.session.refresh_token(self.token_url, refresh_token=refresh_token)
            return new_token
        except OAuth2Error as e:
            raise OAuth2ClientError(f"Error refreshing token: {e}")

    def get(self, url, token):
        """
        使用访问令牌获取资源。

        :param url: 资源URL
        :param token: 访问令牌
        :return: 资源响应的JSON数据
        :raises OAuth2ClientError: 如果获取资源失败
        """
        try:
            self.session.token = token
            response = self.session.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.json()
        except OAuth2Error as e:
            raise OAuth2ClientError(f"Error making GET request: {e}")
        except Exception as e:
            raise OAuth2ClientError(f"HTTP error: {e}")

# # 使用示例
# if __name__ == "__main__":
#     import os

#     client_id = os.getenv("CLIENT_ID")
#     client_secret = os.getenv("CLIENT_SECRET")
#     authorize_url = "https://example.com/oauth/authorize"
#     token_url = "https://example.com/oauth/token"
#     redirect_uri = "https://yourapp.com/callback"
#     scope = "read write"

#     oauth_client = OAuth2Client(client_id, client_secret, authorize_url, token_url, redirect_uri, scope)

#     try:
#         # 获取授权URL
#         auth_url, state = oauth_client.get_authorization_url()
#         print(f"请访问以下URL进行授权: {auth_url}")

#         # 在用户授权后，你会收到一个回调请求，其中包含授权响应
#         authorization_response = input("请输入授权响应URL: ")

#         # 获取访问令牌
#         token = oauth_client.fetch_token(authorization_response)
#         print(f"访问令牌: {token}")

#         # 使用访问令牌获取资源
#         resource_url = "https://example.com/api/resource"
#         response = oauth_client.get(resource_url, token)
#         print(f"资源响应: {response}")
#     except OAuth2ClientError as e:
#         print(f"OAuth2ClientError: {e}")
