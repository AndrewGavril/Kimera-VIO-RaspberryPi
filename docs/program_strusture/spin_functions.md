# Список spin функций

1. DataProviderInterface->spin()

    - Преобразует данные датасета и отправляет правый и левый кадр в соответствующие очереди.

2. EurocdataProvider->spin()

    - Преобразует данные Euroc датасета и отправляет правый и левый кадр в соответствующие очереди.

3. KittiDataProvider->spin() skipped
4. Pipeline->spin()

    - Возвращает результат вызова (class DataProviderModule) data_provider_module->spin()
    
5. PipeLineModule->spin()

    - получает данные из очереди(реализация зависит от конкретного модуля)
    - обрабатывает данные(реализация зависит от конкретного модуля)
    - отправляет на выход(реализация зависит от конкретного модуля)
    
6. PipeLineModuleBase->spin() virtual

# Список spinOnce функций

1. Mesher->spinOnce(input)

    - Сериализация данных
    - Получение полигональной сетки
    - Получение вершинной сетки
    - возвращает результат
    
2. MesherModule->spinOnce(input)
    
    - Возвращает результат Mesher->spinOnce
    
3. VioBackendModule->spinOnce(input)

    - Возвращает результат VioBackend->spinOnce(input)
    
4. VioBackend->spinOnce(input)

    - возвращает облако точек(BackendOtput)
    
5. StereoVisionFrontEnd->spinOnce(input)
    
    - возвращает стереопару кадров с флагом keyFrame
    
6. StereoVisionFrontEndModule->spinOnce(input)

    - возвращает результат StereoVisionFrontEnd->spinOnce(input)
    
7. Pipeline->spinOnce(input)

    - инициализация FrontEnd потока
    - инициализация еще нескольких потоков: backend, mesher, lcd_module, visualizer
    - отправка входного пакета данных в frontend очередь
    
8. Visualizer spins skipped
9. LoopClosureDetector->spinOnce(input)

    - выставление флага - был ли цикл и возврат результата
    
10. EurocDataProvider->spinOnce()

    - проверка для окончания отправки новых кадров