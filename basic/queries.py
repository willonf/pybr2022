from django.db.models import (
    Q, IntegerField, Sum, ExpressionWrapper, F, FloatField, Count, Value, When, Case,
    DateField, DurationField, CharField, Max, Min, Avg, OuterRef, Subquery, Exists)
from django.db.models.functions import Extract, Now, Cast, ExtractDay, LPad, Upper, Lower, Replace

from basic import models


# TODO: Consultas no banco
# O valor armazenado em 'zones' é um QuerySet, uma classe do django cuja função é armazenar consultas.
#  É um iterator. Só é executado quando ocorre alguma operação que utilize o QuerySet
# Quando as queries são muito complexas, o ideal é criar um behavior ou inserir no Manager do model

def all_zones():
    zones = models.Zone.objects.all()
    print(zones)  # Aqui a consulta é realizada, pois a operação foi chamada
    print(zones.query)  # Exibe a string SQL que ele forma
    return zones


def all_zones_with_limit():
    zones = models.Zone.objects.all()[:2]  # Aqui realizamos o slice para obter apenas os 10 primeiros registros
    print(zones)  # Aqui a consulta é realizada, pois a operação foi chamada
    print(zones.query)  # Exibe a string SQL que ele forma
    return zones


# Filter: O .filter() cria uma cláusula where na consulta
def ana_luiza():
    return models.Employee.objects.filter(name='Ana Luiza Cunha')


def employee_id_100():
    return models.Employee.objects.filter(pk=100)


def female_employees():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.FEMALE)


def female_employees2():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.MALE, salary=2097)


# Ordenação (order by)
def ordered_employees_by_salary():
    models.Employee.objects.order_by('salary')
    # ASC. Para DESC coloca-se (-salary). O Django entende que precisa trazer todos.


# Values: diferente dos outros métodos (que retornam um queryset), .values() retorna uma lista de dicionários.
def employees_id_name():
    return models.Employee.objects.values('id', 'name')


# Distinct
def query_distinct():
    return models.SaleItem.objects.values('product__name').order_by('product__name').distinct()


# É possível combinar funções: .filter().values()

# As consultas acima utilizam o AND (&). Para usar o OR (|) utilizamos o Q:

def employee_filter1():
    return models.Employee.objects.filter(Q(name='Silva') | Q(salary=2097))


def employee_filter2():
    return models.Employee.objects.filter(Q(name='Rocha') & Q(salary=2097))


# Outra forma é criarmos um objeto Q e na query passarmos como parâmetro

def employee_filter3():
    conditions = Q()
    conditions.add(Q(salary__gte=1000), Q.AND)
    conditions.add(Q(name='Rocha'), Q.AND)
    return models.Employee.objects.filter(conditions)


# Utilizando o NOT na cláusula WHERE:
# No queryset abaixo, serão pesquisados todos os employees que não são do sexo masculino
def employee_filter4():
    return models.Employee.objects.exclude(gender=models.ModelBase.Gender.MALE)


# TODO: Consultas com fields lookups


def employee_salary_gte_1000():
    return models.Employee.objects.filter(salary__gte=1000)  # __gte: Greater than or equal


def employee_name_icontains_silva():
    return models.Employee.objects.filter(name__icontains='Silva')


# GET: retorna um objeto ao invés de um queryset. Sempre deve retornar um valor único. Lança excessão, usar try catch
def employee_pk_1():
    try:
        models.Department.objects.get(pk=1)
    except models.Employee.DoesNotExist:
        print('Register not found')


# Exercício 1: Todos os funcionários que contenham silva no nome:
def exercicio1():
    return models.Employee.objects.filter(name__icontains='Silva')


# Exercício 2: Todos os funcionários com o salário maior que R$5.000,00
def exercicio2():
    return models.Employee.objects.filter(salary__gt=5000)


# Exercício 3: Todos os clientes que tem uma renda mensal inferior a R$2.000,00
def exercicio3():
    return models.Customer.objects.filter(income__lt=2000)  # __lte: Less than


# Exercício 4: Todos os funcionários admitidos entre 2010 e 2021

def exercicio4():
    return models.Employee.objects.filter(
        admission_date__year__gte=2010, admission_date__year__lte=2021
    ).order_by(
        'admission_date'
    )


# Exercício 4.1: Todos os funcionários admitidos entre 2010 e 2021
def exercicio5():
    return models.Employee.objects.annotate(
        year=Extract(expression='admission_date', lookup_name='year', output_field=IntegerField())
    ).filter(
        year__range=(2010, 2021)
    ).order_by('year')


# Count: retorna um valor inteiro
def employee_count():
    return models.Employee.objects.count()


def employee_filter_count():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.FEMALE).count()


# Exists: retorna True ou False, ou seja, se existem resultados na consulta
def employee_exists():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.MALE).exists()


# First e last: traz o primeiro e último objeto do queryset
def employee_first():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.MALE).first()


def employee_last():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.MALE).last()


# Exercício 5: Criar uma consulta para trazer o total de funcionários por estado civil
def funcionarios_por_estado_civil():
    return models.Employee.objects.values('marital_status__name').annotate(
        marital_status=F('marital_status__name'),
        total=Count(F('id'))
    ).values('marital_status', 'total')


# Exercício 6: Criar uma consulta para trazer o total vendido em valor R$ por filial;
def exercicio6():
    return models.SaleItem.objects.select_related(
        'sale__branch'
    ).values(
        'sale__branch__name'
    ).annotate(
        total=Sum(ExpressionWrapper(
            F('quantity') * F('product__sale_price'), output_field=FloatField()
        ))
    ).values('sale__branch__name', 'total')


# UPDATE
def employee_update1():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.FEMALE).update(active=False)


def employee_update2():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.FEMALE).update(active=True)


# DELETE
def employee_delete():
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.FEMALE).delete()


# Criação de colunas dinâmicas
# Value: usado para colocarmos valores dentro da query
# ExpressionWrapper: utilizado para cálculos dentro da query. Não esquecer de passar o output field
# F: quando queremos usar um field da tabela

def employee_dynamic_field1():
    return models.Employee.objects.annotate(column=Value(10)).values('id', 'name', 'column')


def employee_dynamic_field2():
    return models.Employee.objects.annotate(
        new_salary=ExpressionWrapper(Value(10) + Value(10), output_field=FloatField()))


def employee_dynamic_field3():
    return models.Employee.objects.annotate(
        new_salary=ExpressionWrapper(Value(10) + F('salary'), output_field=FloatField())
    ).values('salary', 'new_salary')


# Exercício 7: Query para retornar o nome do funcionário, o salário atual e salário + 10%
def exercicio7():
    return models.Employee.objects.annotate(
        new_salary=ExpressionWrapper(F('salary') * Value(1.10), output_field=FloatField())
    ).values('name', 'salary', 'new_salary')


# CASE: estruturas condicionais
def employee_case1():
    return models.Employee.objects.annotate(
        gender_description=Case(
            When(gender=models.ModelBase.Gender.MALE, then=Value('Masculino')),
            default=Value('Feminino'))
    ).values('name', 'gender', 'gender_description')


# Exercício 8: Consulta para retornar um status do funcionário de acordo com o seu salário

def exercicio8():
    return models.Employee.objects.annotate(
        status=Case(
            When(salary__lte=2000, then=Value('Vendedor Jr.')),
            When(Q(salary__gt=2000) & Q(salary__lte=5000), then=Value('Vendedor Pleno')),
            default=Value('Vendedor Sênior')
        )
    ).values('name', 'salary', 'status')


# JOINS: Utiliza-se "apenas" dois underlines (__)

def employee_join_department():
    return models.Employee.objects.values('name', 'department', 'department__name')


def employee_join_department_district_city_state1():
    return models.Employee.objects.values('name', 'district__name', 'district__city__name',
                                          'district__city__state__name')


def employee_join_department_district_city_state2():
    return models.Employee.objects.annotate(
        bairro=F('district__name'), cidade=F('district__city__name'),
        estado=F('district__city__state__name')
    ).values('name', 'bairro', 'cidade', 'estado')


def employee_join_department_district_city_state3():
    return models.Employee.objects.values(
        'name', 'district__name', 'district__city__name', 'district__city__state__name')


def employee_join_filter():
    return models.Employee.objects.filter(department__name='Policial federal')


# Join com relação inversa
def department_employees_salary():
    return models.Department.objects.filter(employees__salary__gte=10000)


# Exercício 9: método que receba como param a quantidade de produtos que serão vendidos e retorne uma consulta quanto
# o funcionário irá ganhar de comissão em cada produto
def exercicio9(quantity):
    # Outra solução:
    # return models.Product.objects.annotate(
    #     subtotal=ExpressionWrapper(F('sale_price') * quantity, output_field=FloatField())
    # ).annotate(
    #     comission=ExpressionWrapper((F('subtotal') * F('product_group__commission_percentage') / 100),
    #                                 output_field=FloatField())
    # ).values('name', 'sale_price', 'subtotal', 'product_group__commission_percentage', 'comission')

    # Obs: Na query acima, toda a expressão de 'subtotal' do annotate será chamado novamente em 'comission'
    # Isso não impacta na performance, pois no banco de dados o plano de execução de query para subtotal já terá sido
    # formado e na próxima vez que 'subtotal' for chamado, isso será mais rápido

    return models.Product.objects.annotate(
        comissao=(Value(quantity) * F('sale_price') * F('product_group__commission_percentage')) / Value(100)
    ).values(
        'name', 'comissao', 'sale_price', 'product_group__commission_percentage')


# Exercício 10: fazer uma consulta para retornar todos os funcionários casados ou solteiros
def exercicio10():
    conditions = Q()
    conditions.add(Q(marital_status__name='Solteiro'), Q.OR)
    conditions.add(Q(marital_status__name='Casado'), Q.OR)
    # Outras formas:
    # return models.Employee.objects.filter(
    #     Q(marital_status__name__icontains='Casado') | Q(marital_status__name__icontains='Solteiro')
    # ).values('name', 'marital_status__name')
    #
    # return models.Employee.objects.filter(
    #     marital_status__name__in=['Solteiro', 'Casado']
    # ).values('name', 'marital_status__name')

    return models.Employee.objects.filter(conditions).values('name', 'marital_status__name')


# Exercício 12: Fazer uma consulta para retornar todos os funcionários que ganham entre R$1000 e R$5000
def exercicio12():
    # return models.Employee.objects.filter(salary__range=(1000, 5000)).values('name', 'salary')
    return models.Employee.objects.filter(Q(salary__gte=1000) & Q(salary__lte=5000)).values('name', 'salary')


# Exercício 13: Fazer uma consulta que retorne a diferença do preço de custo e preço de venda dos produtos;
def exercicio13():
    return models.Product.objects.annotate(
        profit=ExpressionWrapper(F('sale_price') - F('cost_price'), output_field=FloatField())
    ).values(
        'name', 'sale_price', 'cost_price', 'profit'
    )


# Exercício 14: Fazer uma consulta para retornar todos os funcionários que não tenham salário entre R$4000 e R$8000
def exercicio14():
    conditions = Q()
    conditions.add(Q(salary__gte=4000), Q.AND)
    conditions.add(Q(salary__lte=8000), Q.AND)
    return models.Employee.objects.exclude(conditions).values('name', 'salary')


# Exercício 15: Fazer uma consulta para retornar todas as vendas dentre 2010 e 2021
def exercicio15():
    return models.Sale.objects.filter(
        Q(date__year__gte=2010) & Q(date__year__lte=2021)
    ).values(
        'id', 'date'
    )


# Exercício 16: Fazer uma consulta que retorne o tipo de funcionário de acordo com sua idade:
#   18 - 25: Jr. | 26 - 34: Pl. | 35 ou mais: Sr.
def exercicio16():
    # Outra forma:
    # Usando func: o func executa uma função que tem no database, mas não tem no Django
    # Obs.: Incompleto
    #
    # return models.Employee.objects.annotate(
    #     age=ExtractYear(Func(F('birth_date'), function='age', output_field=DurationField()))
    # ).values('name', 'age', 'birth_date')

    return models.Employee.objects.annotate(
        diff=ExpressionWrapper(Cast(Now(), output_field=DateField()) - F('birth_date'), output_field=DurationField()),
        age=ExpressionWrapper(ExtractDay('diff') / 365, output_field=IntegerField()),
        status=Case(
            When(age__range=(18, 25), then=Value('Vendedor Jr.')),
            When(age__range=(26, 34), then=Value('Vendedor Pleno')),
            When(age__gte=35, then=Value('Vendedor Sênior')),
            default=Value('Não identificado')
        )
    ).values('name', 'age', 'status')


# Exercício 17: fazer uma consulta para retornar um status para o funcionário de acordo com o tempo de casa:
#   Até 2 anos: Novato | Acima de 2 e menor ou igual a 5 anos: Intermediário | Acima de 5 anos: Veterano
def exercicio17():
    return models.Employee.objects.annotate(
        diff=ExpressionWrapper(Cast(Now(), output_field=DateField()) - F('admission_date'),
                               output_field=DurationField()),
        work_age=ExpressionWrapper(ExtractDay('diff') / 365, output_field=IntegerField()),
        status=Case(
            When(work_age__lte=2, then=Value('Novato')),
            When(work_age__range=(3, 5), then=Value('Intermediário')),
            When(work_age__gt=5, then=Value('Veterano')),
            default=Value('Não identificado')
        )
    ).values('name', 'work_age', 'status')


# Prefetch related: Usado no "lado" N das relaões
# "Department" pode conter N "Employee": usar prefetch_related
# "Employee" pode conter 1 "Department": usar select_related
def query_prefetch_related():
    return models.Department.objects.prefetch_related(
        'employees').filter(
        employees__salary__gte=2000
    ).values(
        'name',
        'employees__name'
    )


# Lpad
def query_lpad():
    return models.Employee.objects.annotate(
        code=LPad(
            expression=Cast(F('id'), output_field=CharField()),
            length=5,
            fill_text=Value('0'))
    ).values('code', 'id')


# UpperCase e LowerCase
def query_upper_case():
    return models.Employee.objects.annotate(
        _upper=Upper('name'),
        _lower=Lower('name')
    ).values('name', '_upper', '_lower')


# TODO: FUNÇÕES DE AGRUPAMENTO

def query_max_employee_salary():
    # Aggregate: vai agregar os dados de Employee. Já é executado na declaração,
    # mas é possível mudar esse comportamento nos settings.
    # Deve ser chamado no final da query.
    # Geralmente não é utilizado para agrupar, pois não retorna um queryset.
    # O ideal é utilizar quando queremos retornar um valor único apenas
    return models.Employee.objects.aggregate(
        max=Max('salary')
    )


def query_min_employee_salary():
    # Aggregate: vai agregar os dados de Employee
    return models.Employee.objects.aggregate(
        min=Min('salary')
    )


def query_avg_employee_salary():
    # Aggregate: vai agregar os dados de Employee
    return models.Employee.objects.aggregate(
        average=Avg('salary')
    )


def query_count_employee_salary():
    # Aggregate: vai agregar os dados de Employee
    return models.Employee.objects.aggregate(
        count=Count('salary')
    )


def query_count_employee_female_salary():
    # Aggregate: vai agregar os dados de Employee
    return models.Employee.objects.filter(gender=models.ModelBase.Gender.FEMALE).aggregate(
        count=Count('*')
    )


# TODO: group by - essa cláusula é feita na query inserindo um values() antes do annotate
# Exercício 18: consulta para saber a soma dos salários por departamento
def query_total_salary_per_department():
    # O select_related foi usado para não haver duplicidade na consulta
    return models.Employee.objects.select_related('department').values('department__name').annotate(
        sum=Sum('salary')
    ).values('department__name', 'sum')


def query_total_salary_per_department_and_gender():
    return models.Employee.objects.select_related('department').values('department__name', 'gender').annotate(
        sum=Sum('salary')
    ).values('department__name', 'sum', 'gender').order_by('department__name')


# Exercício 19: fazer uma consulta para retornar o nome do funcionário e o bairro onde ele mora;
def exercicio19():
    return models.Employee.objects.annotate(
        bairro=F('district__name')
    ).values('name', 'bairro')


# Exercício 20: Fazer uma consulta para retornar o nome do cliente, cidade e zona que mesmo mora;
def exercicio20():
    return models.Customer.objects.annotate(
        customer_city=F('district__city__name'),
        customer_zone=F('district__zone__name'),
    ).values('name', 'customer_city', 'customer_zone')


# Exercício 21: Fazer uma consulta para retornar os dados da filial: nome, estado e cidade onde a mesma está localizada;
def exercicio21():
    return models.Branch.objects.annotate(
        branch_city=F('district__city__name'),
        branch_state=F('district__city__state__name'),
    ).values('name', 'branch_city', 'branch_state')


# Exercício 22: fazer uma consulta para retornar os dados do funcionário: nome,
# departamento onde ele trabalha e qual seu estado civil atual;
def exercicio22():
    return models.Employee.objects.values('name', 'department__name', 'marital_status__name')


# Exercício 23: Fazer uma consulta para retornar o nome do produto vendido,
# o preço unitário e o subtotal;
def exercicio23():
    # Sem agrupamento de produto:
    # return models.SaleItem.objects \
    #     .annotate(subtotal=ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField())) \
    #     .values('product__name', 'product__sale_price', 'subtotal')

    # Agrupando por produto:
    return models.SaleItem.objects \
        .annotate(subtotal=ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField())) \
        .values('product__name') \
        .annotate(total=Sum('subtotal')) \
        .values('product__name', 'product__sale_price', 'total')


# Exercício: fazer uma consulta para retornar o nome do produto,
# subtotal e quanto deve ser pago de comissão por  cada item
def query_comission():
    return models.SaleItem.objects \
        .annotate(
        subtotal=ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField()),
        commission=ExpressionWrapper(F('subtotal') * (F('product__product_group__commission_percentage') / 100),
                                     output_field=FloatField())) \
        .values('product__name', 'product__sale_price', 'subtotal',
                'product__product_group__commission_percentage', 'commission')


# Exercício 24: fazer uma consulta para retornar o nome do produto, subtotal e quanto foi obtido de lucro por item
def exercicio24():
    return models.SaleItem.objects \
        .annotate(
        subtotal=ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField()),
        gain=ExpressionWrapper(F('subtotal') * (F('product__product_group__gain_percentage') / 100),
                               output_field=FloatField())) \
        .values('product__name', 'product__sale_price', 'subtotal',
                'product__product_group__gain_percentage', 'gain')


# Exercício 25: ranking dos 10 funcionários mais bem pagos;
def exercicio25():
    return models.Employee.objects.order_by('-salary').values('name', 'salary')[:10]


# Exercício 26: trazer do décimo primeiro ao vigésimo funcionário mais bem pago;
def exercicio26():
    return models.Employee.objects.order_by('-salary').values('name', 'salary')[10:20]


# Exercício 27: ranking dos 20 clientes que tem a menor renda mensal;
def exercicio27():
    return models.Customer.objects.order_by('income').values('name', 'income')[:20]


# Exercício 28: Ranking dos produtos mais caros vendidos no ano de 2021
def exercicio28():
    return models.SaleItem.objects \
        .filter(sale__date__year__exact=2021) \
        .values('product__name', 'product__sale_price', 'sale__date__year') \
        .order_by('-product__sale_price')


# Exercício 29: Criar uma consulta para trazer o primeiro nome dos funcionários
# (obs.: remover títulos como Dr., Dra. etc)
def exercicio29():
    pass
    # return models.Employee.objects.annotate(
    #     first_name=
    # ).values('name', 'first_name')


# Exercício 30: Criar uma consulta para trazer o último nome dos clientes

# Exercício 31: Criar uma consulta para trocar quem tenha "Silva" no nome para "Oliveira"
def exercicio31():
    return models.Employee.objects.filter(name__icontains='Silva').annotate(
        new_name=Replace(
            expression='name',
            text=Value('Silva'),
            replacement=Value('Oliveira')
        )
    ).values('name', 'new_name')


# Exercício 32: Criar uma consulta para trazer o total de funcionários por estado civil;
def exercicio32():
    return models.Employee.objects \
        .select_related('marital_status') \
        .values('marital_status') \
        .annotate(total=Count('*')) \
        .values('marital_status__name', 'total')


# Exercício 33: Criar uma consulta para trazer o total vendido em valor R$ por filial;
def exercicio33():
    return models.SaleItem.objects \
        .select_related('sale__branch') \
        .values('sale__branch__name') \
        .annotate(
        total=Sum(ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField()))) \
        .values('sale__branch__name', 'total')


# Exercício 34: Criar uma consulta para trazer o total vendido em valor R$ por zona;
def exercicio34():
    return models.SaleItem.objects \
        .select_related('sale__branch__district__zone') \
        .annotate(subtotal=ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField())) \
        .values('sale__branch__district__zone') \
        .annotate(total=Sum('subtotal')) \
        .values('sale__branch__district__zone__name', 'total')


# Exercício 35: Criar uma consulta para trazer o total vendido em valor R$ por estado;
def exercicio35():
    return models.SaleItem.objects \
        .annotate(
        subtotal=ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField()),
        state_field=F('sale__branch__district__city__state__name')) \
        .values('state_field') \
        .annotate(total=Sum('subtotal')) \
        .values('state_field', 'total')


# Exercício 36: Criar uma consulta para trazer o total vendido em valor R$ por ano
def total_sold_by_year():
    return models.SaleItem.objects.values(
        'sale__date__year'
    ).annotate(
        subtotal=Sum(ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField())),
        year=F('sale__date__year')
    ).values(
        'year', 'subtotal'
    ).order_by('-year')


# TODO: Subqueries
# Exercicio: retornar a lista de produtos e a última vez em que cada um foi vendido
def query_last_sale_of_each_product():
    # O OuterRef é uma referência externa, de outra consulta.
    # Ex.: abaixo, o campo 'id' em OuterRef não é o id de SaleItem
    sbq = models.SaleItem.objects.select_related('sale').filter(product=OuterRef('id')).values('sale__date').order_by(
        '-sale__date')[:1]
    return models.Product.objects.annotate(
        last_sale=Subquery(sbq)  # Aqui, o OuterRef vai entender que o parâmetro id passado, é o id de Product
    ).values('id', 'name', 'last_sale')


# Exercício: retornar a uma lista que mostre se o produto foi vendido ou não em 2020
def sale_products_2020():
    sbq = models.SaleItem.objects.filter(product=OuterRef('id')).filter(sale__date__year=2020)[:1]
    # O Slice acima foi usado, pois basta ter um registro daquela venda em 2020 para atender a condição
    return models.Product.objects.annotate(
        exists=Exists(sbq)
    ).values('id', 'name', 'exists')
    # Podemos também adicionar um .filter(exists=True) ou .filter(exists=False)
    # para exibir apenas as que tiveram vendas (ou não)


# Exercício: retornar a uma lista que mostre se o produto foi vendido ou não em 2020 (utilizando IN)

def sale_products_2020_in():
    sbq = models.SaleItem.objects.filter(sale__date__year=2020).values_list('product', flat=True).distinct()
    # O values_list vai retornar uma lista de id's de produtos. O flat=True retira a chave do dicionário
    return models.Product.objects.filter(id__in=sbq).values('id', 'name').order_by('-name')
