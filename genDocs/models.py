from django.db import models

class Project(models.Model):
    name = models.CharField('Название проекта', max_length=200)
    file_immage = models.CharField('Имя изображения', max_length=200)
    centerW_immage = models.IntegerField('Середина симметрии по вертикали в пикселях')
    name = models.CharField('Название таблицы', max_length=200)
    folder_column = models.CharField('Имя столбца значенями из которого будут использоваться для создания директории в которую будут сохраняться сгенерированные файлы', max_length=200)
    name_column = models.CharField('Имя столбца значения из которого будут браться для создания генерируемых файлов', max_length=200)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

class Column(models.Model):
    table = models.ForeignKey(Project, on_delete = models.CASCADE)
    column = models.CharField('Имя столбца значения из которого будут рисоваться на шаблонном изображении', max_length=200)
    y = models.IntegerField('Отступ от верхнего края изображения')

    class Meta:
        verbose_name = 'Столбец'
        verbose_name_plural = 'Столбцы'
