"""operations that can be reused globally in the project"""


def get_pagination(offset, page_size, paginator, request, object_list):
    page = 1
    if offset != 0:
        page = round(int(offset) / int(page_size)) + 1

    data = paginator.page(page)

    current_site = f"{request.scheme}://{request.META['HTTP_HOST']}{request.path}"
    extra_params = get_params_url(request)
    count = len(object_list)

    next_page = None
    if (0 < offset + page_size < count) or (offset == 0 and page_size < count):
        next_page = f"{current_site}?limit={page_size}&offset={offset + page_size}{extra_params}"

    previous_page = None
    if offset != 0:
        previous_page = f"{current_site}?limit={page_size}&offset={offset - page_size}{extra_params}"

    return count, next_page, previous_page, data


def get_params_url(request):
    params = request.query_params
    params_url = ""

    for param in params:
        if param not in ["limit", "offset"]:
            params_url += f"&{param}={params[param]}"

    return params_url
