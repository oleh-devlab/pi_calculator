from mpmath import mp, mpf, log
import mpmath
import time
import multiprocessing
import json
import os

# All comments are in Ukrainian temporarily

def pi(точність, степінь):
    mp.dps = точність
    n = mpf(12*2**степінь)
    cos = mpf(mpmath.sqrt(3)/2)
    end = int(log((n/12), 2))
    for iter in range(1, (end+1)):
        cos = mpf(mpmath.sqrt(mpf((1+cos)/2)))
    x = mpf(mpmath.sqrt(2-(2*cos)))
    pi_val = mpf((x*n)/2)
    return 1 

def benchmark_worker(j_value):
    """
    Виконує одне обчислення для заданого 'j' і повертає час виконання.
    Ми використовуємо фіксований 'k', оскільки він слабо впливає на загальний час.
    """
    # Використовуємо фіксований коефіцієнт, близький до оптимального
    k = 1.81 
    
    try:
        start_time = time.perf_counter()
        # Викликаємо основну функцію
        pi(int(k * j_value), j_value)
        end_time = time.perf_counter()
        
        seconds = end_time - start_time
        print(f"  Завершено для j={j_value}, час: {seconds:.4f} с")
        return (j_value, seconds, None)
    except Exception as e:
        print(f"  Помилка для j={j_value}: {e}")
        return (j_value, -1, str(e))

# --- Основний блок ---
if __name__ == "__main__":
    # --- НАЛАШТУВАННЯ БЕНЧМАРКУ ---
    # Список значень 'j', для яких ми виміряємо час.
    # Цей набір підібрано так, щоб отримати хороші дані в межах 10 хвилин.
    J_VALUES_TO_TEST = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000]
    
    # Кількість ядер для паралельного запуску тестів
    NUM_CORES = 4
    
    print("🚀 Починаємо збір даних для аналізу продуктивності...")
    print(f"Буде протестовано {len(J_VALUES_TO_TEST)} значень 'j' на {NUM_CORES} ядрах.")
    
    results_data = {}
    
    # Створюємо пул процесів
    with multiprocessing.Pool(processes=NUM_CORES) as pool:
        # pool.map розподілить значення з J_VALUES_TO_TEST між робітниками
        results = pool.map(benchmark_worker, J_VALUES_TO_TEST)
    
    print("\n--- ✅ Збір даних завершено! ---")
    print("Отримані результати (j, час в секундах):")
    
    # Фільтруємо помилкові результати і заповнюємо словник
    valid_results = []
    for j_res, time_res, error_msg in results:
        if not error_msg:
            print(f"  j = {j_res:<5} | Час = {time_res:.4f} с")
            results_data[j_res] = time_res
            valid_results.append((j_res, time_res))

    # Зберігаємо результати у файл для подальшого аналізу
    file_path = "benchmark_results.json"
    try:
        with open(file_path, "w") as f:
            json.dump(results_data, f, indent=4)
        print(f"\n📈 Дані збережено у файл: {file_path}")
        print("Тепер ці дані можна використати для побудови точної моделі.")
    except Exception as e:
        print(f"\nНе вдалося зберегти файл: {e}")