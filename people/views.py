from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Sum, Avg
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from django_journal.permissions import TeacherPermissionsMixin, StudentPermissionsMixin
from django_journal.settings import STUDENT, TEACHER
from people.forms import UserCreateForm, StudentForm, ContactForm, ContactFormSet, StudentFormSet, UserUpdateForm
from people.models import Teacher, Student, Contact, User
from journal.models import Lesson, Score
from utils.service import ScoreJournalMixin


class TeacherListView(LoginRequiredMixin, ListView):
    """Список всех учителей в школе."""
    template_name = 'people/teacher_list.html'

    def get_queryset(self):
        queryset = User.objects.select_related('teacher__group_manager__grade').filter(user_status=TEACHER)
        return queryset


class TeacherDetailView(LoginRequiredMixin, TeacherPermissionsMixin, DetailView):
    """Вывод информации об учителе."""
    model = Teacher
    template_name = 'people/teacher_detail.html'

    def get_queryset(self):
        queryset = User.objects.select_related('teacher__group_manager__grade').filter(user_status=TEACHER)
        return queryset


class StudentDetailView(LoginRequiredMixin, TeacherPermissionsMixin, DetailView):
    """Информация о конкретном ученике."""
    template_name = 'people/student_detail.html'

    def get_queryset(self):
        queryset = User.objects.select_related('student__group__grade', 'contact').filter(user_status=STUDENT)
        return queryset


class StudentLkDetailView(LoginRequiredMixin, StudentPermissionsMixin, ScoreJournalMixin, DetailView):
    """Личный кабинет ученика."""
    template_name = 'people/student_lk.html'
    context_object_name = 'student'

    def get_object(self, queryset=None):
        return User.objects.select_related('student', 'contact').get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(StudentLkDetailView, self).get_context_data(**kwargs)
        date_period = self.create_date_period_list()
        lessons = Lesson.objects.filter(grade__group__students=self.request.user.student.id)
        scores = Score.objects.filter(student_id=self.request.user.pk,
                                      created__in=date_period).values('id', 'lesson_id', 'score', 'created')

        count_scores = scores.values('score').annotate(count_score=Count('score')).order_by('-score')
        total_scores = count_scores.aggregate(sum_count=Sum('count_score'),
                                              sum_score=Avg('score'),
                                              sum_score_percent=Avg('score')*20)

        student_rating = {5: 0, 4: 0, 3: 0, 2: 0}
        for item in count_scores:
            student_rating[item['score']] = item['count_score']

        context['rating'] = student_rating
        context['total_scores'] = total_scores
        context['date_period'] = date_period
        context['lessons'] = lessons
        context['scores_dict'] = self.create_scores_dict(date_period, scores, lessons, 'lesson_id')
        return context


class StudentCreateView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, CreateView):
    """Создание нового ученика."""
    form_class = UserCreateForm
    template_name = 'people/student_create.html'
    success_url = reverse_lazy('student_add')
    success_message = 'Ученик усешно добавлен.'

    def get_context_data(self, **kwargs):
        data = super(StudentCreateView, self).get_context_data(**kwargs)
        data['student_form'] = StudentForm()
        data['contact_form'] = ContactForm()
        return data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        student_form = StudentForm(self.request.POST)
        contact_form = ContactForm(self.request.POST)
        if form.is_valid() and student_form.is_valid() and contact_form.is_valid():
            user = form.save(commit=False)
            user.user_status = STUDENT
            student = student_form.save(commit=False)
            contact = contact_form.save(commit=False)
            student.user = user
            contact.user = user
            user.save()
            student.save()
            contact.save()
            return self.form_valid(form)
        else:
            messages.error(request, 'Ошибка сохранения !')
            return self.render_to_response({'form': form, 'student_form': student_form, 'contact_form': contact_form})


class StudentUpdateView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, UpdateView):
    """Редактирование ученика."""
    model = User
    queryset = User.objects.filter(user_status=STUDENT)
    form_class = UserUpdateForm
    template_name = 'people/student_update.html'
    success_message = 'Данные ученика успешно обновлены.'

    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(self.request.POST)
        student_formset = StudentFormSet(self.request.POST, prefix='student')
        contact_formset = ContactFormSet(self.request.POST, prefix='contact')
        if student_formset.is_valid() and contact_formset.is_valid():
            contact_formset.save()
            student_formset.save()
            return super(StudentUpdateView, self).post(self.request.POST)
        else:
            messages.error(request, 'Ошибка сохранения !')
            return self.render_to_response(
                {'form': form, 'student_form': student_formset, 'contact_form': contact_formset}
            )

    def get_context_data(self, **kwargs):
        data = super(StudentUpdateView, self).get_context_data(**kwargs)
        student_formset = StudentFormSet(queryset=Student.objects.filter(user_id=self.kwargs['pk']), prefix='student')
        contact_formset = ContactFormSet(queryset=Contact.objects.filter(user_id=self.kwargs['pk']), prefix='contact')

        data['student_form'] = student_formset
        data['contact_form'] = contact_formset
        return data

    def get_success_url(self):
        return reverse_lazy('student_update', kwargs={'pk': self.kwargs['pk']})
