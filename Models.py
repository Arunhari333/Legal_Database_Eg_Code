#Case model

class Case(models.Model):
    case_id = models.OneToOneField(User, models.CASCADE,
                             blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    casename = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,
                                     null=True, blank=True)
    country = models.CharField(max_length=200)
    jurisdiction = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    license = models.CharField(max_length=200)
    version = models.FloatCharField()
    # ...
    # ...
    is_published = models.BooleanField()


class CaseQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) | Q(description__icontains=query) | Q(slug__icontains=query))
            qs = qs.filter(or_lookup).distinct()
        return qs


class CaseManager(models.Manager):
    def get_queryset(self):
        return CaseQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

#User Model

class MyUserManager(BaseUserManager):
    def create_user(self, email, extra_field, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            extra_field=extra_field,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, extra_field, password=None):
        user = self.create_user(
            email,
            password=password,
            extra_field=extra_field,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    extra_field = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['extra_field']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin