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
