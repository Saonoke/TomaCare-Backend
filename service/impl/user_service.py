from typing import Optional
from fastapi import Depends, HTTPException
from sqlmodel import Session

from database.repository import UserRepository, UserRepositoryMeta,ImageRepository,ImageRepositoryMeta
from database.schema.auth_schema import UserResponse
from database.schema.user_schema import UserResponseProfile
from model import Users,Images
from service.meta import UserServiceMeta
from utils.hashing import get_password_hash, verify_password
from database.schema import UserUpdate

class UserService(UserServiceMeta):
    _user_repository = UserRepositoryMeta

    def __init__(self, session: Session):
        self.session = session
        self._user_repository = UserRepository(session)
        self._image_repository :ImageRepositoryMeta = ImageRepository(self.session)

    def __user_model2schema(self, model: Users)-> Optional[UserResponseProfile]:
        model_dump = model.model_dump()
        try:
            model_dump['profile_img'] = model.profile.image_path
        except:
            model_dump['profile_img'] = ''

        if model.password != '-':
            model_dump['hasPassword'] = True
        else:
            model_dump['hasPassword'] = False
        return UserResponseProfile(**model_dump)

    def get(self, _id: int):
        try:
            user = self._user_repository.get_by_id(_id)
            if user is None:
                raise HTTPException(status_code=403, detail="User not found.")
            user =  self.__user_model2schema(user)
            return user
        except HTTPException as e:
            raise e

    def edit(self, user_data: UserUpdate, _id: int) -> Users:
        try:
            user_exist = self._user_repository.get_by_email(user_data.email)
            if user_exist and (user_exist.id != _id):
                raise HTTPException(status_code=400, detail="User with this email already exists.")

            user_exist = self._user_repository.get_by_username(user_data.username)
            if user_exist and (user_exist.id != _id):
                raise HTTPException(status_code=400, detail="User with this username already exists.")

            try:
                user_exist = self._user_repository.get_by_id(_id)
                if user_exist and user_exist.profile_img is None:
                    image_id = self._image_repository.create(Images(image_path=user_data.profile_img))
                    data =  Users(id= _id,email=user_data.email,full_name=user_data.full_name,username=user_data.username,profile_img=image_id)
                else : 
                    image = Images(image_path=user_data.profile_img)
                    self._image_repository.edit(user_exist.profile_img, image)
                    data =  Users(id= _id,email=user_data.email,full_name=user_data.full_name,username=user_data.username,profile_img=user_exist.profile_img)
                
                result = self._user_repository.edit(data, _id)
                result = self.__user_model2schema(result)
                self.session.commit()
                return result
            except Exception as e:
                print(e)
                self.session.rollback()
                raise HTTPException(status_code=400, detail="Edit Failed.")

        except HTTPException as e:
            raise e

    def change_password(self, _old_pass: str, _new_pass: str, _id: int):
        try:
            user = self._user_repository.get_by_id(_id)
            if not user:
                raise HTTPException(status_code=403, detail="User not found.")

            if not verify_password(_old_pass, user.password):
                raise HTTPException(status_code=400, detail="Invalid password.")

            new_pass = get_password_hash(_new_pass)
            user.password = new_pass

            res = self.__user_model2schema(self._user_repository.edit(user, _id))
            return res

        except HTTPException as e:
            raise e

    def create_password(self, _pass: str, _id: int):
        try:
            user = self._user_repository.get_by_id(_id)

            if user.password != '-':
                raise HTTPException(status_code=400, detail="Password already set!")

            new_pass = get_password_hash(_pass)
            user.password = new_pass

            return self.__user_model2schema(self._user_repository.edit(user, _id))

        except HTTPException as e:
            raise e
