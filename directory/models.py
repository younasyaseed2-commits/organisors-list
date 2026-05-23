from django.db import models


class District(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Organizer(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name="organizers",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


class Location(models.Model):
    name = models.CharField(max_length=180)
    aliases = models.TextField(
        blank=True,
        help_text="Optional comma-separated local names or spellings, e.g. Malayalam names.",
    )
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name="locations",
        null=True,
        blank=True,
    )
    organizer = models.ForeignKey(
        Organizer,
        on_delete=models.CASCADE,
        related_name="locations",
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "organizer"],
                name="unique_location_per_organizer",
            ),
        ]

    def __str__(self):
        return self.name
