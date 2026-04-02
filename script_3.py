# All comments are in Ukrainian temporarily

def predict_time(j):
    """
    Прогнозує час виконання одного завдання для заданого 'j' на вашому пристрої.
    """
    # Коефіцієнти, отримані з вашого бенчмарку
    a = 5.61e-8
    b = 2.81e-5
    c = -0.77
    
    seconds = a * (j**2) + b * j + c
    return max(0, seconds) # Повертаємо 0, якщо результат негативний

# Приклад використання:
j_to_check = 700500
predicted_seconds = predict_time(j_to_check)
print(f"Орієнтовний час для j={j_to_check}: {predicted_seconds:.2f} секунд (~{predicted_seconds/60:.1f} хвилин)")

# Вивід:
# Орієнтовний час для j=71500: 287.73 секунд (~4.8 хвилин)