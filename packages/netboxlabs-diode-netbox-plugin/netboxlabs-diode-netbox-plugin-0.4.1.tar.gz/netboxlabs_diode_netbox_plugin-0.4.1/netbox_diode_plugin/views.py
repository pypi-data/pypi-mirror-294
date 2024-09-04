#!/usr/bin/env python
# Copyright 2024 NetBox Labs Inc
"""Diode NetBox Plugin - Views."""

from django.shortcuts import render
from django.views.generic import View


class DisplayStateView(View):
    """Display state view."""

    def get(self, request):
        """Render a display state template."""
        return render(request, "diode/display_state.html")
