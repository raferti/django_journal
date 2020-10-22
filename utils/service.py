import datetime


class ScoreJournalMixin:
    def create_date_period_list(self):
        """Создает список дат находящихся между датой начала и окончания."""
        day_delta = datetime.timedelta(days=1)
        try:
            start_date = datetime.datetime.strptime(self.request.GET.get('start-date'), '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(self.request.GET.get('end-date'), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=15)
        return [start_date + i * day_delta for i in range((end_date - start_date).days + 1)]

    @staticmethod
    def create_scores_dict(date_period, scores, grouping_object, grouping_object_name):
        """
        Формирует словарь необходимый для построения таблицы с оценками. Который включает в себя:
        1. Дату (01.01.2020).
        2. Наименование объектов по которым групируются оценки (школьные предметы или ученики).
        3. Кортеж: оценка, id оценки.
        Пример выходного словаря для дальнейшего вывода оценок
        конкретного ученика (объект группировки шольные предметы):
        { '01.01.2020': {'Математика': ('5', 1),'Русский': ('3', 2),'Чтение': ('0', 0))},
        ... }
        Пример выходного словаря для дальнейшего вывода оценок
        конкретного класса по конкретному предмету (объект группировки ученики):
        { '01.01.2020': {'Иванов': ('5', 1), 'Петров': ('0', 0), 'Сидоров': ('0', 0)},
        ... }
        """
        scores_dict = {}
        for date in date_period:
            scores_dict[date] = {}
            for obj in grouping_object:
                scores_dict[date][obj.id] = (0, 0)
                if scores:
                    for score in scores:
                        if obj.id == score[grouping_object_name] and date == score['created']:
                            scores_dict[date][obj.id] = (score['score'], score['id'])
                            break
        return scores_dict
