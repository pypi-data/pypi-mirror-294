
def celsius_para_fahrenheit(temp_em_celsius):
    temp_em_fahrenheit = 1.8 * temp_em_celsius + 32
    return temp_em_fahrenheit

def fahrenheit_para_celsius(temp_em_fahrenheit):
    temp_em_celsius = (temp_em_fahrenheit - 32) / 1.8
    return temp_em_celsius

temp_em_celsius = float(input("Digite a temperatura em °C (celsius) para conversão em °F (fahrenheit): "))
print(f"A temperatura em fahrenheit é: {celsius_para_fahrenheit(temp_em_celsius)} °C")

temp_em_fahrenheit = float(input("Digite a temperatura em ºF (fahrenheit) para conversão em ºC (celsius): "))
print(f"A temperatura em celius é: {fahrenheit_para_celsius(temp_em_fahrenheit)} °F")