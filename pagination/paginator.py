from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger	

class TUIsDPaginator(Paginator):
    def __init__(self, elemList, elemPerPage):
        if(elemPerPage > 0):
            Paginator.__init__(self, elemList, elemPerPage)
        else:
            raise ValueError('Amount of items per page must be greater than 0')
        
        
    def get_elems_from_page(self, page):
        try:
            elems = self.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            elems = self.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            elems = self.page(self.num_pages)
   	
        return elems
