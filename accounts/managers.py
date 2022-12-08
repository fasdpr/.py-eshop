from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,phone_number,email,full_name,password):
        if not phone_number:
            raise ValueError('کاربر باید شماره تلفن داشته باشد')
        if not email:
            raise ValueError('کاربر باید ایمیل داشته باشد')
        if not full_name:
            raise ValueError('کاربر باید نام کامل داشته باشد')

        user=self.model(phone_number=phone_number,email=self.normalize_email(email),full_name=full_name)
        user.set_password(password)

        user.save(using=self._db)

        return user
    def create_superuser(self,phone_number,email,full_name,password):
        user=self.create_user(phone_number,email,full_name,password)
        user.is_admin=True
        user.save(using=self._db)
        return user

