from django.db import models

from basic import managers


class ModelBase(models.Model):
    # TODO: Classe que criar opções (enum). Apenas a nível a de modelo será verificado.
    #  Isso não cria uma contraint do tipo check, por exemplo.
    class Gender(models.TextChoices):
        MALE = ('M', 'Male')
        FEMALE = ('F', 'Female')

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    modified_at = models.DateTimeField(null=False, auto_now=True)
    active = models.BooleanField(null=False, default=True)

    class Meta:
        # TODO: "abstract = True" significa que esse modelo não será implementado no banco
        # Podemos usar False no caso de estarmos trabalhando com banco de dados já existentes
        # para apenas trabalharmos com consultas e não gerenciamento de modelos em banco
        abstract = True


class Department(ModelBase):
    name = models.CharField(max_length=64, null=False, unique=True,
                            error_messages=
                            {'unique': 'This department already exists.'})

    class Meta:
        # TODO: Nome da tabela que esse modelo representará no banco de dados
        db_table = 'department'
        # Verbose name da tabela no singular e plural
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        # TODO: "managed = True" significa que o Django irá gerenciar esse modelo em banco
        managed = True
        # TODO: Aqui podemos adicionar constraints.

    def __str__(self):
        return self.name


class MaritalStatus(ModelBase):
    name = models.CharField(max_length=64, null=False, unique=True)

    class Meta:
        db_table = 'marital_status'
        managed = True

    def __str__(self):
        return self.name


class Zone(ModelBase):
    name = models.CharField(max_length=64, null=False, unique=True)

    class Meta:
        db_table = 'zone'
        managed = True
    #
    # def __str__(self):
    #     return self.name


class State(ModelBase):
    name = models.CharField(max_length=64, null=False, unique=True)
    abbreviation = models.CharField(max_length=2, null=False)

    class Meta:
        db_table = 'state'
        managed = True

    def __str__(self):
        return f'{self.name} - {self.abbreviation}'


class Supplier(ModelBase):
    name = models.CharField(max_length=64, null=False)
    legal_document = models.CharField(max_length=20, null=False, unique=True)

    class Meta:
        db_table = 'supplier'
        managed = True

    def __str__(self):
        return self.name


class ProductGroup(ModelBase):
    name = models.CharField(max_length=64, null=False, unique=True)
    commission_percentage = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    gain_percentage = models.DecimalField(max_digits=6, decimal_places=2, null=False)

    class Meta:
        db_table = 'product_group'
        managed = True

    def __str__(self):
        return self.name


class Product(ModelBase):
    name = models.CharField(max_length=64, null=False)
    cost_price = models.DecimalField(max_digits=16, decimal_places=2, null=False)
    sale_price = models.DecimalField(max_digits=16, decimal_places=2, null=False)
    product_group = models.ForeignKey(
        to='ProductGroup',
        on_delete=models.DO_NOTHING,
        db_column='id_product_group',
        null=False
    )
    supplier = models.ForeignKey(
        to='Supplier',
        on_delete=models.DO_NOTHING,
        db_column='id_supplier',
        null=False
    )

    class Meta:
        db_table = 'product'
        managed = True

    def __str__(self):
        return self.name


class City(ModelBase):
    name = models.CharField(max_length=64, null=False)
    state = models.ForeignKey(
        to='State',
        on_delete=models.DO_NOTHING,
        db_column='id_state',
        null=False
    )

    class Meta:
        db_table = 'city'
        managed = True

    def __str__(self):
        return f'{self.name} - {self.state}'


class District(ModelBase):
    name = models.CharField(max_length=64, null=False)
    city = models.ForeignKey(
        to='City',
        on_delete=models.DO_NOTHING,
        db_column='id_city',
        null=False
    )
    zone = models.ForeignKey(
        to='Zone',
        on_delete=models.DO_NOTHING,
        db_column='id_zone',
        null=False
    )

    class Meta:
        db_table = 'district'
        managed = True

    def __str__(self):
        return self.name


class Employee(ModelBase):
    name = models.CharField(max_length=64, null=False)
    salary = models.DecimalField(max_digits=16, decimal_places=2, null=False)
    gender = models.CharField(max_length=1, null=False, choices=ModelBase.Gender.choices)
    admission_date = models.DateField(null=False)
    birth_date = models.DateField(null=False)
    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        db_column='id_district',
        null=False
    )
    department = models.ForeignKey(
        to='Department',
        on_delete=models.DO_NOTHING,
        db_column='id_department',
        null=False,
        # TODO: Related name é o nome dado à relação inversa a ser chamada em department:
        # department.employees.all()
        # Valor padrão quando não declarado: employee_set
        related_name='employees'
    )
    marital_status = models.ForeignKey(
        to='MaritalStatus',
        on_delete=models.DO_NOTHING,
        db_column='id_marital_status',
        null=False
    )

    class Meta:
        db_table = 'employee'
        managed = True

    # def __str__(self):
    #     return self.name

    def increase_salary(self, percentage):
        self.salary += self.salary * (percentage / 100)


class Branch(ModelBase):
    name = models.CharField(max_length=64, null=False, unique=True)
    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        db_column='id_district',
        null=False
    )

    class Meta:
        db_table = 'branch'
        managed = True

    def __str__(self):
        return self.name


class Customer(ModelBase):
    name = models.CharField(max_length=64, null=False)
    income = models.DecimalField(max_digits=16, decimal_places=2, null=False)
    gender = models.CharField(max_length=1, null=False, choices=ModelBase.Gender.choices)
    district = models.ForeignKey(
        to='District',
        on_delete=models.DO_NOTHING,
        db_column='id_district',
        null=False
    )
    marital_status = models.ForeignKey(
        to='MaritalStatus',
        on_delete=models.DO_NOTHING,
        db_column='id_marital_status',
        null=False
    )

    class Meta:
        db_table = 'customer'
        managed = True

    def __str__(self):
        return self.name


class Sale(ModelBase):
    date = models.DateTimeField(null=False, auto_now_add=True)
    customer = models.ForeignKey(
        to='Customer',
        on_delete=models.DO_NOTHING,
        db_column='id_customer',
        null=False
    )
    employee = models.ForeignKey(
        to='Employee',
        on_delete=models.DO_NOTHING,
        db_column='id_employee',
        null=False
    )
    branch = models.ForeignKey(
        to='Branch',
        on_delete=models.DO_NOTHING,
        db_column='id_branch',
        null=False
    )
    # Associando manager customizado. Obs.: não substitui os métodos padrões do manager
    objects = managers.SaleManager()

    class Meta:
        db_table = 'sale'
        managed = True


class SaleItem(ModelBase):
    sale = models.ForeignKey(
        to='Sale',
        on_delete=models.DO_NOTHING,
        db_column='id_sale',
        null=False
    )
    product = models.ForeignKey(
        to='Product',
        on_delete=models.DO_NOTHING,
        db_column='id_product',
        null=False
    )
    quantity = models.DecimalField(max_digits=16, decimal_places=3, null=False)
    # O preço do produto deve ser persistido aqui, pois caso haja atualização do preço do produto
    # o valor da venda estará incorreto.
    # Para isso, podemos usar um receiver. Sempre que um SaleItem for criado, ele salva o preço do produto
    product_price = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        null=False,
        default=0
    )

    # TODO: Associando manager customizado. Obs.: não substitui os métodos padrões do manager
    # objects = path_to_a_queryset.as_manager()
    objects = managers.SaleItemManager()

    class Meta:
        db_table = 'sale_item'
        managed = True


# TODO: Exemplos de tabela associativa e unique_together_error
# Também é possível criar um modelo com models.ManyToManyField, caso queiramos deixar isso
# sendo referenciado pelo Django. A forma abaixo é "controlada" pelo próprio desenvolvedor
'''
class Student(ModelBase):
    name = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'student'
        managed = True


class Course(ModelBase):
    name = models.CharField(max_length=64, null=False)

    # Adding ManyToManyField
    # students = models.ManyToManyField(
    #     to='Student',
    #     through = 'StudentCourse'
    # )

    class Meta:
        db_table = 'course'
        managed = True


class StudentCourse(ModelBase):
    student = models.ForeignKey(to='Student', null=False, db_column='id_student', on_delete=models.DO_NOTHING)
    course = models.ForeignKey(to='Course', null=False, db_column='id_course', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'student_course'
        managed = True
        unique_together = [('student', 'course')]
        
        # Se o model herda de um django.forms.ModelForm, podemos usar:
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'Student and course must be uniques'
            }
        }

    # def unique_error_message(self, model_class, unique_check):
    #     if model_class == type(self) and unique_check == ('student', 'course'):
    #         return 'Must be unique'
    #     else:
    #         return super(StudentCourse, self).unique_error_message(model_class, unique_check)
'''
