import django.contrib.auth.mixins
import django.shortcuts
import django.views
import django.views.generic

import menu.forms
import menu.models
import rating.forms
import users.forms
import users.models


class MenuView(
    django.views.generic.TemplateView,
    django.contrib.auth.mixins.LoginRequiredMixin,
):
    template_name = "menu/menu.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breakfast"] = (
            menu.models.BreakfastMenu.objects.select_related(
                "drink1",
                "drink2",
                "dish1",
                "dish2",
            ).first()
        )

        context["lunch"] = menu.models.LunchMenu.objects.select_related(
            "drink1",
            "drink2",
            "soup1",
            "soup2",
            "main",
            "salad1",
            "salad2",
        ).first()

        return context


class DishDetailView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.DetailView,
    django.views.generic.FormView,
):
    model = menu.models.Dish
    template_name = "menu/dish_detail.html"
    context_object_name = "dish"
    queryset = menu.models.Dish.objects.get_queryset()
    form_class = rating.forms.RatingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.rating is not None:
            context["user_mark_id"] = self.rating.pk

        if self.rating_params is not None:
            context["rating_params"] = self.rating_params

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method == "POST":
            self.object = self.get_object()

        self.rating_params = self.object.ratings.aggregate(
            avg_mark=django.db.models.Avg("mark"),
            count_mark=django.db.models.Count("mark"),
        )
        if self.request.user.is_anonymous:
            self.rating = None
        else:
            self.rating = self.object.ratings.filter(
                user=self.request.user,
            ).first()
            kwargs["instance"] = self.rating

        return kwargs

    def form_valid(self, form):
        if self.rating is not None:
            rating = self.rating
            rating.mark = form.cleaned_data.get("mark")
            rating.comment = form.cleaned_data.get("comment")
        else:
            rating = form.save(commit=False)
            rating.user = self.request.user
            rating.dish = self.object

        rating.save()

        return super().form_valid(form)

    def get_success_url(self):
        return django.urls.reverse_lazy(
            "menu:dish_detail",
            kwargs={"pk": self.object.pk},
        )


class EditBreakfastMenuView(
    django.views.View,
    users.forms.RoleRequiredMixin,
):
    required_roles = [
        users.models.Role.RoleNames.ADMIN,
    ]
    template_name = "menu/edit.html"

    def get(self, request):
        total_menu, _ = menu.models.BreakfastMenu.objects.get_or_create(
            pk=1,
        )
        form = menu.forms.BreakfastMenuForm(instance=total_menu)

        return django.shortcuts.render(
            request,
            self.template_name,
            {"form": form},
        )

    def post(self, request):
        total_menu, _ = menu.models.BreakfastMenu.objects.get_or_create(pk=1)
        form = menu.forms.BreakfastMenuForm(request.POST, instance=total_menu)
        if form.is_valid():
            form.save()
            return django.shortcuts.redirect("menu:menu")

        return django.shortcuts.render(
            request,
            self.template_name,
            {"form": form},
        )


class EditLunchMenuView(django.views.View):
    template_name = "menu/edit.html"

    def get(self, request):
        total_menu, _ = menu.models.LunchMenu.objects.get_or_create(pk=1)
        form = menu.forms.LunchMenuForm(instance=total_menu)
        return django.shortcuts.render(
            request,
            self.template_name,
            {"form": form},
        )

    def post(self, request):
        total_menu, _ = menu.models.LunchMenu.objects.get_or_create(pk=1)
        form = menu.forms.LunchMenuForm(request.POST, instance=total_menu)
        if form.is_valid():
            form.save()
            return django.shortcuts.redirect("menu:menu")

        return django.shortcuts.render(
            request,
            self.template_name,
            {"form": form},
        )
