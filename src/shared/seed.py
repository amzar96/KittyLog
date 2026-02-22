import logging
import uuid

from sqlalchemy.orm import Session

from src.shared.models.rbac import Permission, Role, RolePermission
from src.shared.models.subscription import Plan, PlanPermission

logger = logging.getLogger(__name__)

ACTIONS = ["can_read", "can_create", "can_edit", "can_delete", "can_export"]
RESOURCES = [
    "cat", "health", "weight", "vaccine", "nutrition",
    "diary", "monitoring", "appointment", "notification", "photo",
    "user", "role", "plan",
]

FREE_RESOURCES = ["cat", "health", "weight", "vaccine", "diary", "notification"]
FREE_ACTIONS = ["can_read", "can_create", "can_edit", "can_delete"]

ROLES = [
    {"name": "admin", "description": "All permissions on all resources. Bypasses plan restrictions.", "is_default": False},
    {"name": "owner", "description": "Full CRUD on own cats and all related data.", "is_default": True},
    {"name": "viewer", "description": "Read-only access to shared cats.", "is_default": False},
]

OWNER_RESOURCES = [
    "cat", "health", "weight", "vaccine", "nutrition",
    "diary", "monitoring", "appointment", "notification", "photo",
]


def seed_permissions(db: Session) -> dict[str, str]:
    existing = db.query(Permission).filter(Permission.is_deleted == False).all()  # noqa: E712
    if existing:
        logger.info("Permissions already seeded (%d found)", len(existing))
        return {f"{p.action}:{p.resource}": p.id for p in existing}

    permission_map = {}
    for action in ACTIONS:
        for resource in RESOURCES:
            perm = Permission(
                id=str(uuid.uuid4()),
                action=action,
                resource=resource,
                created_by="SYSTEM",
            )
            db.add(perm)
            permission_map[f"{action}:{resource}"] = perm.id

    db.flush()
    logger.info("Seeded %d permissions", len(permission_map))
    return permission_map


def seed_roles(db: Session, permission_map: dict[str, str]) -> dict[str, str]:
    existing = db.query(Role).filter(Role.is_deleted == False).all()  # noqa: E712
    if existing:
        logger.info("Roles already seeded (%d found)", len(existing))
        return {r.name: r.id for r in existing}

    role_map = {}
    for role_data in ROLES:
        role = Role(
            id=str(uuid.uuid4()),
            name=role_data["name"],
            description=role_data["description"],
            is_default=role_data["is_default"],
            created_by="SYSTEM",
        )
        db.add(role)
        role_map[role_data["name"]] = role.id

    db.flush()

    for action in ACTIONS:
        for resource in RESOURCES:
            key = f"{action}:{resource}"
            if key in permission_map:
                rp = RolePermission(
                    id=str(uuid.uuid4()),
                    role_id=role_map["admin"],
                    permission_id=permission_map[key],
                    created_by="SYSTEM",
                )
                db.add(rp)

    for action in ACTIONS:
        for resource in OWNER_RESOURCES:
            key = f"{action}:{resource}"
            if key in permission_map:
                rp = RolePermission(
                    id=str(uuid.uuid4()),
                    role_id=role_map["owner"],
                    permission_id=permission_map[key],
                    created_by="SYSTEM",
                )
                db.add(rp)

    for resource in OWNER_RESOURCES:
        key = f"can_read:{resource}"
        if key in permission_map:
            rp = RolePermission(
                id=str(uuid.uuid4()),
                role_id=role_map["viewer"],
                permission_id=permission_map[key],
                created_by="SYSTEM",
            )
            db.add(rp)

    db.flush()
    logger.info("Seeded %d roles with permissions", len(role_map))
    return role_map


def seed_plans(db: Session, permission_map: dict[str, str]) -> dict[str, str]:
    existing = db.query(Plan).filter(Plan.is_deleted == False).all()  # noqa: E712
    if existing:
        logger.info("Plans already seeded (%d found)", len(existing))
        return {p.name: p.id for p in existing}

    plans = [
        {"name": "free", "description": "Up to 2 cats, basic health/weight tracking, diary (text only)", "price": 0.0},
        {"name": "premium", "description": "Unlimited cats, photos, Google Calendar sync, stock alerts, export, anomaly detection", "price": 9.99},
    ]

    plan_map = {}
    for plan_data in plans:
        plan = Plan(
            id=str(uuid.uuid4()),
            name=plan_data["name"],
            description=plan_data["description"],
            price=plan_data["price"],
            is_active=True,
            created_by="SYSTEM",
        )
        db.add(plan)
        plan_map[plan_data["name"]] = plan.id

    db.flush()

    for action in FREE_ACTIONS:
        for resource in FREE_RESOURCES:
            key = f"{action}:{resource}"
            if key in permission_map:
                pp = PlanPermission(
                    id=str(uuid.uuid4()),
                    plan_id=plan_map["free"],
                    permission_id=permission_map[key],
                    created_by="SYSTEM",
                )
                db.add(pp)

    for action in ACTIONS:
        for resource in RESOURCES:
            key = f"{action}:{resource}"
            if key in permission_map:
                pp = PlanPermission(
                    id=str(uuid.uuid4()),
                    plan_id=plan_map["premium"],
                    permission_id=permission_map[key],
                    created_by="SYSTEM",
                )
                db.add(pp)

    db.flush()
    logger.info("Seeded %d plans with permissions", len(plan_map))
    return plan_map


def run_seed(db: Session) -> None:
    logger.info("Starting database seed...")
    permission_map = seed_permissions(db)
    seed_roles(db, permission_map)
    seed_plans(db, permission_map)
    db.commit()
    logger.info("Database seed completed")
