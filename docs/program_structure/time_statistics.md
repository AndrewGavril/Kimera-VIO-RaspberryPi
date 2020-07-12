# Измерение времени исполнения
## Отметки по времени для различных модулей
VioFrontEnd Frame Rate и VioFrontEnd Keyframe Rate замеряются в функции spinOnce класса StereoVisionFrontEnd ([здесь](https://github.com/AndrewGavril/Kimera-VIO-RaspberryPi/blob/master/src/frontend/StereoVisionFrontEnd.cpp#L85) начинается отсчет времени обработки одного кадра). В конце обработки отсчет относится к Frame Rate или Keyframe Rate в зависимости от параметра is\_keyframe\_.

Остальные отметки (исполнение отдельных модулей) установлены в общей для всех модулей функции [spin](https://github.com/AndrewGavril/Kimera-VIO-RaspberryPi/blob/master/include/kimera-vio/pipeline/PipelineModule.h#L194) и измеряют время одной итерации при наличии входных данных.

## Вычисление частоты
После сбора всех временных отрезков среднее время выполнения вычисляется с помощью функции [Mean](https://github.com/AndrewGavril/Kimera-VIO-RaspberryPi/blob/master/include/kimera-vio/utils/Accumulator.h#L94), а частота с помощью функции [MeanCallsPerSec](https://github.com/AndrewGavril/Kimera-VIO-RaspberryPi/blob/master/include/kimera-vio/utils/Statistics.h#L102).
