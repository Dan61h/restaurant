from django.core.paginator import Paginator
from django.db.models import Model
from django.shortcuts import render

# Возвращает массив номеров страниц дл¤ перехода
# -1 - троеточие
#
# curPage - текущий номер страницы
# itemsPerPage - количество элементов на странице
# itemsCount - общее количество элементов

def GetPageNumsToShow(curPage, itemsPerPage, itemsCount):
	totalPages = (max(itemsCount - 1, 0) // itemsPerPage) + 1
	if totalPages > 7:
		left = curPage - 2
		right = curPage + 2
		res = [1]
		if left > 2:
			res.append(-1)
		res += list(range(max(left, 2), min(right, totalPages - 1) + 1))
		if right < totalPages - 1:
			res.append(-1)
		res.append(totalPages)
		return res
	else:
		return list(range(1, totalPages + 1))


def RenderWithPaging(request, template, context, data, perPage):
    try:
        page = int(request.GET.get("page", default = 1))
        dataPage = Paginator(data, perPage).get_page(page)
        pageNums = GetPageNumsToShow(page, perPage, data.count())
        itemStartFrom = (page - 1) * perPage
        
        if "page" in request.GET:
            getWithoutPage = request.GET.copy()
            del getWithoutPage["page"]
            pageLink = request.path + "?" + getWithoutPage.urlencode()
        else:
            getWithoutPage = request.GET
            pageLink = request.get_full_path()

            if len(getWithoutPage) == 0:
                pageLink += "?"

        pageLink += "&page=" if len(getWithoutPage) > 0 else "page="

        pageContext = {
            "pageItemStartFrom": itemStartFrom,
            "pageData": dataPage,
            "pageNumbers": pageNums,
            "curPage": page,
            "perPage": perPage,
            "pageLink": pageLink
        }
        newContext = dict(pageContext, **context)
        return render(request, template, newContext)
    except:
        return render(request, template, dict({ "pageData": [] }, **context))


def GetFormSingleError(form):
    return list(form.errors.values())[0][0]


def SetModelFromDict(modelInst, vals):
    fieldNames = { field.verbose_name for field in modelInst._meta.fields }
    
    for fldName, fldValue in vals.items():
        if fldName in fieldNames:
            setattr(modelInst, fldName, fldValue)
