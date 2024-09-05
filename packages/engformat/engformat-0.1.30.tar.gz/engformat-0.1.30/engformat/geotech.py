

def add_gwl_symbol(subplot, x_rel, y_actual, zorder=None, **kwargs):
    xlims = subplot.get_xlim()
    if zorder:
        kwargs['zorder'] = zorder
    subplot.text(xlims[0] + (xlims[1] - xlims[0]) * x_rel, y_actual, '$\\nabla$', **kwargs)
