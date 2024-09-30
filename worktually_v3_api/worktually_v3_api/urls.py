from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Schema Views for Each App
employee_schema_view = get_schema_view(
    openapi.Info(
        title="Employee API",
        default_version="v1",
        description="API documentation for Employee management",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@employees.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path("api/", include("employee.urls"))],
)

recruitment_schema_view = get_schema_view(
    openapi.Info(
        title="Recruitment API",
        default_version="v1",
        description="API documentation for Recruitment management",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@recruitment.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path("", include("recruitment.urls"))],
)

job_seekers_schema_view = get_schema_view(
    openapi.Info(
        title="Job Seekers API",
        default_version="v1",
        description="API documentation for Job Seekers",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@jobseekers.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path("", include("job_seekers.urls"))],
)

lookups_schema_view = get_schema_view(
    openapi.Info(
        title="Lookups API",
        default_version="v1",
        description="API documentation for Lookups management",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@lookups.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path("", include("lookups.urls"))],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Include API paths for each app
    path("api/", include("employee.urls")),
    path("", include("recruitment.urls")),
    path("", include("job_seekers.urls")),
    path("", include("lookups.urls")),
    # Swagger and ReDoc UIs for Employee
    re_path(
        r"^swagger/employee(?P<format>\.json|\.yaml)$",
        employee_schema_view.without_ui(cache_timeout=0),
        name="schema-employee-json",
    ),
    path(
        "swagger/employee/",
        employee_schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-employee-swagger-ui",
    ),
    path(
        "redoc/employee/",
        employee_schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-employee-redoc",
    ),
    # Swagger and ReDoc UIs for Recruitment
    re_path(
        r"^swagger/recruitment(?P<format>\.json|\.yaml)$",
        recruitment_schema_view.without_ui(cache_timeout=0),
        name="schema-recruitment-json",
    ),
    path(
        "swagger/recruitment/",
        recruitment_schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-recruitment-swagger-ui",
    ),
    path(
        "redoc/recruitment/",
        recruitment_schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-recruitment-redoc",
    ),
    # Swagger and ReDoc UIs for Job Seekers
    re_path(
        r"^swagger/jobseekers(?P<format>\.json|\.yaml)$",
        job_seekers_schema_view.without_ui(cache_timeout=0),
        name="schema-jobseekers-json",
    ),
    path(
        "swagger/jobseekers/",
        job_seekers_schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-jobseekers-swagger-ui",
    ),
    path(
        "redoc/jobseekers/",
        job_seekers_schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-jobseekers-redoc",
    ),
    # Swagger and ReDoc UIs for Lookups
    re_path(
        r"^swagger/lookups(?P<format>\.json|\.yaml)$",
        lookups_schema_view.without_ui(cache_timeout=0),
        name="schema-lookups-json",
    ),
    path(
        "swagger/lookups/",
        lookups_schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-lookups-swagger-ui",
    ),
    path(
        "redoc/lookups/",
        lookups_schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-lookups-redoc",
    ),
]
