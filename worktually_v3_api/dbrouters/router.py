class MyDatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ["auth", "admin", "sessions", "contenttypes"]:
            return "default"
        if model._meta.app_label in ["employee"]:
            return "default"
        if model._meta.app_label in ["job_seekers", "recruitment", "lookups"]:
            return "global"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ["auth", "admin", "sessions", "contenttypes"]:
            return "default"
        if model._meta.app_label in ["employee"]:
            return "default"
        if model._meta.app_label in ["job_seekers", "recruitment", "lookups"]:
            return "global"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in [
            "auth",
            "admin",
            "sessions",
            "contenttypes",
        ] or obj2._meta.app_label in ["auth", "admin", "sessions", "contenttypes"]:
            return True
        if obj1._meta.app_label == "employee" and obj2._meta.app_label == "employee":
            return True
        if obj1._meta.app_label in [
            "job_seekers",
            "recruitment",
            "lookups",
        ] and obj2._meta.app_label in ["job_seekers", "recruitment", "lookups"]:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in ["auth", "admin", "sessions", "contenttypes"]:
            return db == "default"
        if app_label == "employee":
            return db == "default"
        if app_label in ["job_seekers", "recruitment", "lookups"]:
            return db == "global"
        return None
