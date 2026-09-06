from pydantic import BaseModel


class EstadoActivoMixin:
    """Utilidades para manejar el estado activo/inactivo de un usuario."""

    def activate(self):
        self.is_active = True
        return self

    def deactivate(self):
        self.is_active = False
        return self

    def toggle_active(self) -> bool:
        self.is_active = not self.is_active
        return self.is_active

    @property
    def estado(self) -> str:
        return "activo" if self.is_active else "inactivo"


#Función post
class UserCreate(BaseModel):
    nombre: str
    edad: int
    region: str
    email: str


#Función get
class UserResponse(EstadoActivoMixin, BaseModel):
    id: int
    nombre: str
    edad: int
    region: str
    email: str
    is_active: bool  # <-- NUEVO CAMPO: Muestra si el usuario está activo o borrado lógicamente

    class Config:
        from_attributes = True
        orm_mode = True


class UserUpdate(EstadoActivoMixin, BaseModel):
    nombre: str | None = None
    edad: int | None = None
    region: str | None = None
    email: str | None = None
    is_active: bool | None = None
