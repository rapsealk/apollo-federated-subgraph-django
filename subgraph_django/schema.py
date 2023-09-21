import logging
from uuid import uuid4

import graphene
from graphene_django import DjangoObjectType
from graphene_federation import build_schema, key

from subgraph_django.users.models import Job as JobModel

log = logging.getLogger(__name__)


@key(fields="id")
class Job(DjangoObjectType):
    class Meta:
        name = JobModel.__name__
        model = JobModel
        interfaces = (graphene.relay.Node,)
        connection_class = graphene.relay.Connection
        fields = "__all__"

    def __resolve_reference(self, info, **kwargs):
        """
        Here we resolve the reference of the user entity referenced by its `id` field.
        """
        print(f"Job.subgraph.resolve() kwargs={kwargs}")
        return Job(id=self.id)


class Query(graphene.ObjectType):
    job = graphene.Field(Job)
    jobs = graphene.List(Job)

    def resolve_job(self, info, **kwargs):
        print(f"Query.resolve_job() kwargs={kwargs}")
        job = JobModel.objects.create()
        return job

    def resolve_jobs(self, info, **kwargs):
        print(f"Query.resolve_jobs() kwargs={kwargs}")
        return JobModel.objects.all()


schema = build_schema(query=Query, enable_federation_2=True)
