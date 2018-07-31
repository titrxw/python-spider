class UserInfo(object):
    _userName=''
    _userPwd=''

    def __init__(self,userName,userPwd):
        self._userName=userName
        self._userPwd=userPwd

    def getUserName(self):
        return self._userName

    def getUserPwd(self):
        return self._userPwd

    def setUserName(self,userName):
        self._userName=userName

    def setUserPwd(self,userPwd):
        self._userPwd=userPwd