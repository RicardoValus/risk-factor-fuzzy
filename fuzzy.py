import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definir os Antecedentes e Consequentes
umidade = ctrl.Antecedent(np.arange(0, 101, 1), 'umidade')
precipitacao = ctrl.Antecedent(np.arange(0, 101, 1), 'precipitacao')
vrf = ctrl.Consequent(np.arange(0, 101, 1), 'vrf')

# Definir funções de pertinência
umidade['baixa'] = fuzz.trimf(umidade.universe, [0, 0, 50])
umidade['media'] = fuzz.trimf(umidade.universe, [0, 50, 100])
umidade['alta'] = fuzz.trimf(umidade.universe, [50, 100, 100])

precipitacao['baixa'] = fuzz.trimf(precipitacao.universe, [0, 0, 50])
precipitacao['media'] = fuzz.trimf(precipitacao.universe, [0, 50, 100])
precipitacao['alta'] = fuzz.trimf(precipitacao.universe, [50, 100, 100])

vrf['baixo'] = fuzz.trimf(vrf.universe, [0, 0, 50])
vrf['medio'] = fuzz.trimf(vrf.universe, [0, 50, 100])
vrf['alto'] = fuzz.trimf(vrf.universe, [50, 100, 100])

# Definir regras
rule1 = ctrl.Rule(umidade['baixa'] & precipitacao['baixa'], vrf['alto'])
rule2 = ctrl.Rule(umidade['media'] & precipitacao['media'], vrf['medio'])
rule3 = ctrl.Rule(umidade['alta'] & precipitacao['alta'], vrf['baixo'])

# Adicionar as regras ao sistema de controle
vrf_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
vrf_simulation = ctrl.ControlSystemSimulation(vrf_ctrl)

def simular_vrf(umidade_valor, precipitacao_valor):
    vrf_simulation.input['umidade'] = umidade_valor
    vrf_simulation.input['precipitacao'] = precipitacao_valor
    vrf_simulation.compute()
    return vrf_simulation.output['vrf']

# Testar com valores de entrada
umidade_valor = 40
precipitacao_valor = 10

try:
    vrf_valor = simular_vrf(umidade_valor, precipitacao_valor)
    print(f"Variação do Fator de Risco (VRF) para umidade {umidade_valor}% e precipitação {precipitacao_valor}mm é: {vrf_valor:.2f}")
except Exception as e:
    print(f"Erro durante a simulação: {e}")

