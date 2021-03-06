from sqlalchemy.exc import IntegrityError
import graphene
from config.helpers import check_email
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from config.database import db_session
from flask_graphql_auth import create_access_token, create_refresh_token, mutation_header_jwt_refresh_token_required, get_jwt_identity, query_header_jwt_required, mutation_header_jwt_required
from .serializer import UserType

class Register(graphene.Mutation):
    success = graphene.Boolean()
    error = graphene.String()
    message = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    @classmethod
    def mutate(cls, _, info, username, email, password1, password2, first_name, last_name):
        if not check_email(email):
            return Register(error="Make sure you pass correct email.")
        
        if password1 != password2:
            return Register(error="Password did not match.")
        try:
            new_user = User(
                username = username,
                email = email,
                password = generate_password_hash(password1, method='sha256'),
                first_name = first_name,
                last_name = last_name
            )

            db_session.add(new_user)
            db_session.commit()
            return Register(success = True, message="User created")
        except IntegrityError as e:
            return Register(error=f"{e.orig}")

class AuthMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()
    error = graphene.String()

    @classmethod
    def mutate(cls, _, info, email, password):
        if not check_email(email):
            return AuthMutation(error="Invalid email")

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return AuthMutation(error="Bad username or password")

        return AuthMutation(
            access_token = create_access_token(user.id),
            refresh_token = create_refresh_token(user.id)
        )

class RefreshMutation(graphene.Mutation):
    access_token = graphene.String()
    refresh_token = graphene.String()
    error = graphene.String()

    @classmethod
    @mutation_header_jwt_refresh_token_required
    def mutate(cls, info):
        try:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)
            refresh_token = create_refresh_token(identity=current_user)
            return RefreshMutation(access_token=access_token, refresh_token=refresh_token)
        except IntegrityError as e:
            return RefreshMutation(error=f"{e.orig}")

class UpdateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        email = graphene.String()
        password1 = graphene.String()
        password2 = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()
    error = graphene.String()
    
    @classmethod
    @mutation_header_jwt_required
    def mutate(cls, _, info, username, email, password1, password2, first_name, last_name):
        userData = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password1': password1,
            'password2': password2
        }
        if not check_email(email):
            return UpdateUser(error="Make sure you pass correct email.")
        
        if password1 != password2:
            return UpdateUser(error="Password did not match.")
        try:
            isUpdated = False
            user_id = get_jwt_identity()
            user = User.query.filter_by(id=user_id).first()
            for property in userData.keys():
                if (property in ['password1', 'password2']):
                    password = generate_password_hash(password1, method='sha256')
                    setattr(user, 'password', password)
                elif (getattr(user, property) == userData[property]):
                    continue
                else:
                    setattr(user, property, userData[property])
                isUpdated = True
            db_session.commit()
            if (isUpdated):
                return UpdateUser(success=True, message=f"User has been updated.")
            return UpdateUser(success=True, message=f"Nothing to update user data.")
        except IntegrityError as e:
            return UpdateUser(error=f"{e.orig}")

class DeleteUser(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    error = graphene.String()
    
    @classmethod
    @mutation_header_jwt_required
    def mutate(cls, _, info):
        try:
            user_id = get_jwt_identity()
            user = User.query.filter_by(id=user_id).first()
            db_session.delete(user)
            db_session.commit()
            return DeleteUser(success=True, message="User deleted.")
        except IntegrityError as e: 
            return DeleteUser(error=f"{e.orig}", success=False)


class Mutation(graphene.ObjectType):
    register = Register.Field()
    auth = AuthMutation.Field()
    refresh = RefreshMutation.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

class Query(graphene.ObjectType):
    me = graphene.Field(UserType)

    @classmethod
    @query_header_jwt_required
    def resolve_me(cls, _, info):
        user_id = get_jwt_identity()
        return User.query.filter_by(id=user_id).first()