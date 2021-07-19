from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

# Template tag to get the svg icons used, here we can put all svg code and then
# return it to template wrapped with right tag.
# To add a new svg icon just put the <path></path> tag into a dictionary.
# You can get svg icons in https://tabler-icons.io/


@register.simple_tag(name='svg_icon')
def svg_icon(icon_name, extra_class='', id=''):
    icons = {
        'home': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path> <polyline points="5 12 3 12 12 3 21 12 19 12"></polyline> <path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-7"></path> <path d="M9 21v-6a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v6"></path>',

        'dashboard': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="12" cy="13" r="2"></circle><line x1="13.45" y1="11.55" x2="15.5" y2="9.5"></line><path d="M6.4 20a9 9 0 1 1 11.2 0z"></path>',

        'edit': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M9 7h-3a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-3"></path><path d="M9 15h3l8.5 -8.5a1.5 1.5 0 0 0 -3 -3l-8.5 8.5v3"></path><line x1="16" y1="5" x2="19" y2="8"></line>',

        'delete': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><line x1="4" y1="7" x2="20" y2="7"></line><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line><path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12"></path><path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3"></path>',

        'settings': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 -2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z"></path><circle cx="12" cy="12" r="3"></circle>',

        'logout': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M14 8v-2a2 2 0 0 0 -2 -2h-7a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2 -2v-2"></path><path d="M7 12h14l-3 -3m0 6l3 -3"></path>',

        'login': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M14 8v-2a2 2 0 0 0 -2 -2h-7a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2 -2v-2"></path><path d="M20 12h-13l3 -3m0 6l-3 -3"></path>',

        'arrow_back': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M9 11l-4 4l4 4m-4 -4h11a4 4 0 0 0 0 -8h-1"></path>',

        'plus': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line>',

        'info_circle': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="12" cy="12" r="9"></circle><line x1="12" y1="8" x2="12.01" y2="8"></line><polyline points="11 12 12 12 12 16 13 16"></polyline>',

        'external_link': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M11 7h-5a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-5"></path><line x1="10" y1="14" x2="20" y2="4"></line><polyline points="15 4 20 4 20 9"></polyline>',

        'link': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M10 14a3.5 3.5 0 0 0 5 0l4 -4a3.5 3.5 0 0 0 -5 -5l-.5 .5"></path><path d="M14 10a3.5 3.5 0 0 0 -5 0l-4 4a3.5 3.5 0 0 0 5 5l.5 -.5"></path>',

        'refresh': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M20 11a8.1 8.1 0 0 0 -15.5 -2m-.5 -4v4h4"></path><path d="M4 13a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4"></path>',

        'check': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M5 12l5 5l10 -10"></path>',

        'checks': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M7 12l5 5l10 -10"></path><path d="M2 12l5 5m5 -5l5 -5"></path>',

        'coin': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="12" cy="12" r="9"></circle><path d="M14.8 9a2 2 0 0 0 -1.8 -1h-2a2 2 0 0 0 0 4h2a2 2 0 0 1 0 4h-2a2 2 0 0 1 -1.8 -1"></path><path d="M12 6v2m0 8v2"></path>',

        'wallet': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M17 8v-3a1 1 0 0 0 -1 -1h-10a2 2 0 0 0 0 4h12a1 1 0 0 1 1 1v3m0 4v3a1 1 0 0 1 -1 1h-12a2 2 0 0 1 -2 -2v-12"></path><path d="M20 12v4h-4a2 2 0 0 1 0 -4h4"></path>',

        'currency_real': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M21 6h-4a3 3 0 0 0 0 6h1a3 3 0 0 1 0 6h-4"></path><path d="M4 18v-12h3a3 3 0 1 1 0 6h-3c5.5 0 5 4 6 6"></path><path d="M18 6v-2"></path><path d="M17 20v-2"></path>',

        'user': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="12" cy="7" r="4"></circle><path d="M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2"></path>',

        'users': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="9" cy="7" r="4"></circle><path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path><path d="M21 21v-2a4 4 0 0 0 -3 -3.85"></path>',

        'browser': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><rect x="4" y="4" width="16" height="16" rx="1"></rect><line x1="4" y1="8" x2="20" y2="8"></line><line x1="8" y1="4" x2="8" y2="8"></line>',

        'files': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M15 3v4a1 1 0 0 0 1 1h4"></path><path d="M18 17h-7a2 2 0 0 1 -2 -2v-10a2 2 0 0 1 2 -2h4l5 5v7a2 2 0 0 1 -2 2z"></path><path d="M16 17v2a2 2 0 0 1 -2 2h-7a2 2 0 0 1 -2 -2v-10a2 2 0 0 1 2 -2h2"></path>',

        'file_invoice': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M14 3v4a1 1 0 0 0 1 1h4"></path><path d="M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2z"></path><line x1="9" y1="7" x2="10" y2="7"></line><line x1="9" y1="13" x2="15" y2="13"></line><line x1="13" y1="17" x2="15" y2="17"></line>',

        'bell': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M10 5a2 2 0 0 1 4 0a7 7 0 0 1 4 6v3a4 4 0 0 0 2 3h-16a4 4 0 0 0 2 -3v-3a7 7 0 0 1 4 -6"></path><path d="M9 17v1a3 3 0 0 0 6 0v-1"></path>',

        'search': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="10" cy="10" r="7"></circle><line x1="21" y1="21" x2="15" y2="15"></line>',

        'brand_github': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M9 19c-4.3 1.4 -4.3 -2.5 -6 -3m12 5v-3.5c0 -1 .1 -1.4 -.5 -2c2.8 -.3 5.5 -1.4 5.5 -6a4.6 4.6 0 0 0 -1.3 -3.2a4.2 4.2 0 0 0 -.1 -3.2s-1.1 -.3 -3.5 1.3a12.3 12.3 0 0 0 -6.2 0c-2.4 -1.6 -3.5 -1.3 -3.5 -1.3a4.2 4.2 0 0 0 -.1 3.2a4.6 4.6 0 0 0 -1.3 3.2c0 4.6 2.7 5.7 5.5 6c-.6 .6 -.6 1.2 -.5 2v3.5"></path>',

        'brand_google': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M17.788 5.108a9 9 0 1 0 3.212 6.892h-8"></path>',

        'heart': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M19.5 13.572l-7.5 7.428l-7.5 -7.428m0 0a5 5 0 1 1 7.5 -6.566a5 5 0 1 1 7.5 6.572"></path>',

        'shield_lock': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M12 3a12 12 0 0 0 8.5 3a12 12 0 0 1 -8.5 15a12 12 0 0 1 -8.5 -15a12 12 0 0 0 8.5 -3"></path><circle cx="12" cy="11" r="1"></circle><line x1="12" y1="12" x2="12" y2="14.5"></line>',

        'alert-triangle': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M12 9v2m0 4v.01"></path><path d="M5 19h14a2 2 0 0 0 1.84 -2.75l-7.1 -12.25a2 2 0 0 0 -3.5 0l-7.1 12.25a2 2 0 0 0 1.75 2.75"></path>',

        'clear-all': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M8 6h12"></path><path d="M6 12h12"></path><path d="M4 18h12"></path>',

        'download': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2 -2v-2"></path><polyline points="7 11 12 16 17 11"></polyline><line x1="12" y1="4" x2="12" y2="16"></line>',

        'bug': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M9 9v-1a3 3 0 0 1 6 0v1"></path><path d="M8 9h8a6 6 0 0 1 1 3v3a5 5 0 0 1 -10 0v-3a6 6 0 0 1 1 -3"></path><line x1="3" y1="13" x2="7" y2="13"></line><line x1="17" y1="13" x2="21" y2="13"></line><line x1="12" y1="20" x2="12" y2="14"></line><line x1="4" y1="19" x2="7.35" y2="17"></line><line x1="20" y1="19" x2="16.65" y2="17"></line><line x1="4" y1="7" x2="7.75" y2="9.4"></line><line x1="20" y1="7" x2="16.25" y2="9.4"></line>',

        'trending_down': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><polyline points="3 7 9 13 13 9 21 17"></polyline><polyline points="21 10 21 17 14 17"></polyline>',

        'trending_up': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><polyline points="3 17 9 11 13 15 21 7"></polyline><polyline points="14 7 21 7 21 14"></polyline>',

        'minus': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><line x1="5" y1="12" x2="19" y2="12"></line>',

        'motorbike': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="5" cy="16" r="3"></circle><circle cx="19" cy="16" r="3"></circle><path d="M7.5 14h5l4 -4h-10.5m1.5 4l4 -4"></path><path d="M13 6h2l1.5 3l2 4"></path>',

        'template': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><rect x="4" y="4" width="16" height="4" rx="1"></rect><rect x="4" y="12" width="6" height="8" rx="1"></rect><line x1="14" y1="12" x2="20" y2="12"></line><line x1="14" y1="16" x2="20" y2="16"></line><line x1="14" y1="20" x2="20" y2="20"></line>',

        'product': '<path stroke="none" d="M0 0h24v24H0z" fill="none"/>'
                   '<path d="M10 16v-8h2.5a2.5 2.5 0 1 1 0 5h-2.5" />'
                   '<circle cx="12" cy="12" r="9" />',

        'map': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><polyline points="3 7 9 4 15 7 21 4 21 17 15 20 9 17 3 20 3 7"></polyline><line x1="9" y1="4" x2="9" y2="17"></line><line x1="15" y1="7" x2="15" y2="20"></line>',

        'diamond': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M6 5h12l3 5l-8.5 9.5a0.7 .7 0 0 1 -1 0l-8.5 -9.5l3 -5"></path><path d="M10 12l-2 -2.2l.6 -1"></path>',

        'comet': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M15.5 18.5l-3 1.5l.5 -3.5l-2 -2l3 -.5l1.5 -3l1.5 3l3 .5l-2 2l.5 3.5z"></path><line x1="4" y1="4" x2="11" y2="11"></line><line x1="9" y1="4" x2="12.5" y2="7.5"></line><line x1="4" y1="9" x2="7.5" y2="12.5"></line>',

        'cash': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><rect x="7" y="9" width="14" height="10" rx="2"></rect><circle cx="14" cy="14" r="2"></circle><path d="M17 9v-2a2 2 0 0 0 -2 -2h-10a2 2 0 0 0 -2 2v6a2 2 0 0 0 2 2h2"></path>',

        'notes': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><rect x="5" y="3" width="14" height="18" rx="2"></rect><line x1="9" y1="7" x2="15" y2="7"></line><line x1="9" y1="11" x2="15" y2="11"></line><line x1="9" y1="15" x2="13" y2="15"></line>',

        'receipt': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M5 21v-16a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v16l-3 -2l-2 2l-2 -2l-2 2l-2 -2l-3 2m4 -14h6m-6 4h6m-2 4h2"></path>',

        'building_factory': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M4 21c1.147 -4.02 1.983 -8.027 2 -12h6c.017 3.973 .853 7.98 2 12"></path><path d="M12.5 13h4.5c.025 2.612 .894 5.296 2 8"></path><path d="M9 5a2.4 2.4 0 0 1 2 -1a2.4 2.4 0 0 1 2 1a2.4 2.4 0 0 0 2 1a2.4 2.4 0 0 0 2 -1a2.4 2.4 0 0 1 2 -1a2.4 2.4 0 0 1 2 1"></path><line x1="3" y1="21" x2="22" y2="21"></line>',

        'calendar': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><rect x="4" y="5" width="16" height="16" rx="2"></rect><line x1="16" y1="3" x2="16" y2="7"></line><line x1="8" y1="3" x2="8" y2="7"></line><line x1="4" y1="11" x2="20" y2="11"></line><line x1="11" y1="15" x2="12" y2="15"></line><line x1="12" y1="15" x2="12" y2="18"></line>',

        'eye': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><circle cx="12" cy="12" r="2"></circle><path d="M22 12c-2.667 4.667 -6 7 -10 7s-7.333 -2.333 -10 -7c2.667 -4.667 6 -7 10 -7s7.333 2.333 10 7"></path>',

        'report_money': '<path stroke="none" d="M0 0h24v24H0z" fill="none"></path><path d="M9 5h-2a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-12a2 2 0 0 0 -2 -2h-2"></path><rect x="9" y="3" width="6" height="4" rx="2"></rect><path d="M14 11h-2.5a1.5 1.5 0 0 0 0 3h1a1.5 1.5 0 0 1 0 3h-2.5"></path><path d="M12 17v1m0 -8v1"></path>'
    }

    svg_tag = format_html(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round" class="icon {extra}" id="{id}"> {icon} </svg>', extra=extra_class, icon=mark_safe(icons[icon_name]), id=id)

    return svg_tag
