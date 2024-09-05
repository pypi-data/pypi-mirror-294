import httpx
import json

class AbstractApi(object) :
    def getAccessToken(self) :
        raise NotImplementedError

    def refreshAccessToken(self) :
        raise NotImplementedError

    def getSuiteAccessToken(self) :
        raise NotImplementedError

    def refreshSuiteAccessToken(self) :
        raise NotImplementedError

    def getProviderAccessToken(self) :
        raise NotImplementedError

    def refreshProviderAccessToken(self) :
        raise NotImplementedError

    @staticmethod
    def __tokenExpired(errCode):
        """检查令牌是否过期"""
        return errCode in [40014, 42001, 42007, 42009]

    def __refreshToken(self, url) :
        if 'SUITE_ACCESS_TOKEN' in url :
            self.refreshSuiteAccessToken()
        elif 'PROVIDER_ACCESS_TOKEN' in url :
            self.refreshProviderAccessToken()
        elif 'ACCESS_TOKEN' in url :
            self.refreshAccessToken()

    @staticmethod
    def __checkResponse(response):
        '''
        :param response: 请求返回结果
        '''
        errCode = response.get('errcode')
        errMsg = response.get('errmsg')

        if errCode == 0:
            return response 
        else:
            raise RuntimeError(errCode, errMsg)

    def httpCall(self, urlType, params:dict, req_body=None, **kwargs) -> json:
        '''
        :param urlType: 请求地址类型
        :param params: 请求参数
        :param req_body: 请求体
        :param kwargs: 其他参数
        :return: json
        '''
        url = urlType[0]
        method = urlType[1]
        response = {}
        for retryCnt in range(0, 3) :
            if 'POST' == method and req_body is not None:
                response = self.__httpPost(url, params, req_body, **kwargs)
            elif 'GET' == method :
                response = self.__httpGet(url, params, **kwargs)
            # check if token expired
            if self.__tokenExpired(response.get('errcode')) :
                self.__refreshToken(url)
                retryCnt += 1
                continue
            else :
                break

        return self.__checkResponse(response) 

    def __httpPost(self, url:str, params:dict, req_body, **kwargs) -> json:
        """
        :param url: 请求地址
        :param params: 请求参数
        :param req_body: 请求体
        :param kwargs: 其他参数
        :return: json
        """
        try:
            response_data = httpx.post(url, params=params, json=req_body, **kwargs)
            json_data = response_data.json()
        except (httpx.ConnectError, httpx.HTTPError, httpx.ProtocolError,
                httpx.InvalidURL, httpx.TimeoutException, httpx.NetworkError,
                httpx.ProxyError) as err:
            raise RuntimeError("error", err)

        return json_data


    def __httpGet(self, url:str, params:dict, **kwargs) -> json:
        """
        :param url: 请求地址
        :param params: 请求参数
        :param kwargs: 其他参数
        :return: json
        """
        try:
            response_data = httpx.get(url, params=params, **kwargs)
            json_data = response_data.json()
        except (httpx.ConnectError, httpx.HTTPError, httpx.ProtocolError,
                httpx.InvalidURL, httpx.TimeoutException, httpx.NetworkError,
                httpx.ProxyError) as err:
            raise RuntimeError("error", err)
        return json_data

    def __httpPostFile(self, url, media_file):
        return httpx.post(url, file=media_file).json()
