# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.1
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _extra
else:
    import _extra

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "this":
            set(self, name, value)
        elif name == "thisown":
            self.this.own(value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)



# pylint: disable=all


def page_merge(doc_des, doc_src, page_from, page_to, rotate, links, copy_annots, graft_map):
    return _extra.page_merge(doc_des, doc_src, page_from, page_to, rotate, links, copy_annots, graft_map)

def JM_merge_range(doc_des, doc_src, spage, epage, apage, rotate, links, annots, show_progress, graft_map):
    return _extra.JM_merge_range(doc_des, doc_src, spage, epage, apage, rotate, links, annots, show_progress, graft_map)

def FzDocument_insert_pdf(doc, src, from_page, to_page, start_at, rotate, links, annots, show_progress, final, graft_map):
    return _extra.FzDocument_insert_pdf(doc, src, from_page, to_page, start_at, rotate, links, annots, show_progress, final, graft_map)

def page_xref(this_doc, pno):
    return _extra.page_xref(this_doc, pno)

def _newPage(*args):
    return _extra._newPage(*args)

def JM_add_annot_id(annot, stem):
    return _extra.JM_add_annot_id(annot, stem)

def JM_get_annot_id_list(page):
    return _extra.JM_get_annot_id_list(page)

def _add_caret_annot(*args):
    return _extra._add_caret_annot(*args)

def Tools_parse_da(this_annot):
    return _extra.Tools_parse_da(this_annot)

def Annot_getAP(annot):
    return _extra.Annot_getAP(annot)

def Tools_update_da(this_annot, da_str):
    return _extra.Tools_update_da(this_annot, da_str)

def JM_point_from_py(p):
    return _extra.JM_point_from_py(p)

def Annot_rect(annot):
    return _extra.Annot_rect(annot)

def util_transform_rect(rect, matrix):
    return _extra.util_transform_rect(rect, matrix)

def Annot_rect3(annot):
    return _extra.Annot_rect3(annot)

def Page_derotate_matrix(*args):
    return _extra.Page_derotate_matrix(*args)

def JM_get_annot_xref_list(page_obj):
    return _extra.JM_get_annot_xref_list(page_obj)

def xref_object(*args):
    return _extra.xref_object(*args)

def Link_is_external(this_link):
    return _extra.Link_is_external(this_link)

def Page_addAnnot_FromString(*args):
    return _extra.Page_addAnnot_FromString(*args)

def Link_next(this_link):
    return _extra.Link_next(this_link)

def page_count_fz2(document):
    return _extra.page_count_fz2(document)

def page_count_fz(document):
    return _extra.page_count_fz(document)

def page_count_pdf(pdf):
    return _extra.page_count_pdf(pdf)

def page_count(*args):
    return _extra.page_count(*args)

def page_annot_xrefs(*args):
    return _extra.page_annot_xrefs(*args)

def Outline_is_external(outline):
    return _extra.Outline_is_external(outline)

def Document_extend_toc_items(*args):
    return _extra.Document_extend_toc_items(*args)

def ll_fz_absi(i):
    return _extra.ll_fz_absi(i)

def JM_new_texttrace_device(out):
    return _extra.JM_new_texttrace_device(out)

def JM_char_bbox(line, ch):
    return _extra.JM_char_bbox(line, ch)

def JM_char_quad(line, ch):
    return _extra.JM_char_quad(line, ch)

def JM_print_stext_page_as_text(res, page):
    return _extra.JM_print_stext_page_as_text(res, page)

def set_skip_quad_corrections(on):
    return _extra.set_skip_quad_corrections(on)

def set_subset_fontnames(on):
    return _extra.set_subset_fontnames(on)

def set_small_glyph_heights(on):
    return _extra.set_small_glyph_heights(on)

def JM_cropbox(page_obj):
    return _extra.JM_cropbox(page_obj)

def get_cdrawings(page, extended=None, callback=None, method=None):
    return _extra.get_cdrawings(page, extended, callback, method)

def JM_make_spanlist(line_dict, line, raw, buff, tp_rect):
    return _extra.JM_make_spanlist(line_dict, line, raw, buff, tp_rect)

def extractWORDS(this_tpage, delimiters):
    return _extra.extractWORDS(this_tpage, delimiters)

def extractBLOCKS(_self):
    return _extra.extractBLOCKS(_self)

def link_uri(link):
    return _extra.link_uri(link)

def page_get_textpage(_self, clip, flags, matrix):
    return _extra.page_get_textpage(_self, clip, flags, matrix)

def JM_make_textpage_dict(tp, page_dict, raw):
    return _extra.JM_make_textpage_dict(tp, page_dict, raw)

def pixmap_pixel(pm, x, y):
    return _extra.pixmap_pixel(pm, x, y)

def pixmap_n(pixmap):
    return _extra.pixmap_n(pixmap)

def JM_search_stext_page(page, needle):
    return _extra.JM_search_stext_page(page, needle)

def set_pixel(pm, x, y, color):
    return _extra.set_pixel(pm, x, y, color)

def fz_new_image_from_compressed_buffer(w, h, bpc, colorspace, xres, yres, interpolate, imagemask, buffer, mask):
    return _extra.fz_new_image_from_compressed_buffer(w, h, bpc, colorspace, xres, yres, interpolate, imagemask, buffer, mask)

def rearrange_pages2(doc, new_pages):
    return _extra.rearrange_pages2(doc, new_pages)

