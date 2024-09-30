import logging
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from employee.models import Employee, Role_has_Permission, Permission

logger = logging.getLogger(__name__)


class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        required_permission = view_kwargs.get("required_permission", None)

        if required_permission:
            # Get the token from the Authorization header
            auth_header = request.headers.get("Authorization", None)
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse(
                    {"message": "Authentication credentials were not provided."},
                    status=401,
                )

            token = auth_header.split(" ")[1]

            try:
                # Decode the token
                decoded_token = AccessToken(token)
                user_id = decoded_token.get("user_id")
                role = decoded_token.get("role")

                logger.debug(f"Decoded User ID: {user_id}")
                logger.debug(f"Decoded Role: {role}")

                # Retrieve the user from the Employee model
                user = Employee.objects.get(id=user_id)
                user_role = user.role  # Ensure `role` field exists in Employee model

                logger.debug(f"User Role: {user_role}")

                if not self.has_permission(user_role, required_permission):
                    logger.warning(
                        f"User {user_id} with role {user_role} does not have permission {required_permission}"
                    )
                    return JsonResponse(
                        {
                            "message": "Forbidden: You do not have permission to perform this action."
                        },
                        status=403,
                    )

            except Employee.DoesNotExist:
                return JsonResponse({"message": "User does not exist."}, status=403)
            except Exception as e:
                logger.error(f"Error processing token: {e}")
                return JsonResponse(
                    {"message": "Token is invalid or expired."}, status=401
                )

        return None

    def has_permission(self, role, permission_name):
        try:
            permission = Permission.objects.get(name=permission_name)
            return Role_has_Permission.objects.filter(
                role=role, permission=permission
            ).exists()
        except Permission.DoesNotExist:
            logger.error(f"Permission {permission_name} does not exist")
            return False
