from Control.ValidaReglasNegocio import Validador_Reglas_Negocio
from Control.Clientes import *
from Control.InterfaceBanco import Api_Mantenimiento, Api_Transacciones
from Entity.DaoBaseDatos import Dao_Nosql
from Entity.BaseDatos import Gestor_BD
import pytest

class TestClass:

    data = {"rut": 495, "nombre": "Fabian", "edad": 19, "sueldo": 1000000}
    data_monto = {"rut": 495, "nombre": "Fabian", "edad": 19, "sueldo": 500000, "monto": 120000}

    @pytest.fixture
    def instancia_validador(self):
        return Validador_Reglas_Negocio()
    
    @pytest.fixture
    def instancia_cliente_cuenta(self):
        return Cliente_Cuenta(210, "Raul", 40, 1000000)
    
    @pytest.fixture
    def instancia_banco_comercial(self):
        return Banco_Comercial()

    @pytest.fixture
    def instancia_dao(self):
        gestor = Gestor_BD()
        return Dao_Nosql(gestor_BD=gestor)

    @pytest.mark.parametrize("edad, expected_output", [(19, True),(58, True),(32, True)])
    def test_validar_edad(self, edad, expected_output, instancia_validador):
        assert instancia_validador.validar_edad(edad=edad) == expected_output

    @pytest.mark.parametrize("sueldo, expected_output", [(1500000, True), (983000, True), (1000000, True)])
    def test_validar_sueldo(self, instancia_validador, sueldo, expected_output):
        assert instancia_validador.validar_sueldo(sueldo=sueldo) == expected_output

    @pytest.mark.parametrize("monto, expected_output", [(20000, True), (150000, True)])
    def test_validar_monto_deposito(self, monto, expected_output, instancia_validador):
        assert instancia_validador.validar_monto_deposito(monto) == expected_output

    def test_fabrica_banco_comercial(self):
        cliente_cuenta = Banco_Comercial()
        cliente_cuenta = cliente_cuenta.crea_cliente_cuenta(numero=930, nombre="Hector", edad=33, sueldo=550000)
        assert isinstance(cliente_cuenta, Cliente_Cuenta)

    def test_consultar_BD(self, instancia_dao):
        cliente = Banco_Comercial()
        cliente_nuevo = cliente.crea_cliente_cuenta(numero=200, nombre="Ibrahim", edad=20, sueldo=100000)
        assert instancia_dao.consultar(cliente_nuevo) == None
    
    def test_grabar_BD(self, instancia_dao):
        cliente = Banco_Comercial()
        cliente_nuevo = cliente.crea_cliente_cuenta(numero=200, nombre="Ibrahim", edad=20, sueldo=100000)
        assert instancia_dao.grabar(cliente_nuevo) is None
    
    def test_crear_instrumento(self):
        api_mantenimiento = Api_Mantenimiento()
        assert api_mantenimiento.crea_instrumento(data=self.data) == True

    def test_modificar_bd(self, instancia_dao):
        cliente = Banco_Comercial()
        cliente_nuevo = cliente.crea_cliente_cuenta(numero=200, nombre="Ibrahim", edad=20, sueldo=100000)
        assert instancia_dao.modificar(cliente_nuevo) == cliente_nuevo

    def test_credita_cuenta(self):
        cliente = Banco_Comercial()
        cliente_nuevo = cliente.crea_cliente_cuenta(numero=200, nombre="Ibrahim", edad=20, sueldo=100000)
        saldo_antiguo = cliente_nuevo.saldo
        cliente_nuevo.credita_cuenta(monto=20000)
        assert cliente_nuevo.muestra_saldo() > saldo_antiguo

    # Falla
    def test_incrementa_instrumento(self):
        data = {495: {"saldo": 120000}}
        api_transacciones = Api_Transacciones()
        assert api_transacciones.incrementa_instrumento(data=self.data_monto) == True, data