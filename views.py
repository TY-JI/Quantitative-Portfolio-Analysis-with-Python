import numpy as np

class View:
    def __init__(self, view_type, asset_1, value, asset_2=None):
        if view_type not in ('absolute','relative'):
            raise ValueError(
                f'Unknown view type : {view_type}'
            )

        self.view_type = view_type
        self.asset_1 = asset_1
        self.asset_2 = asset_2
        self.value = value

    def p_row(self, tickers):
        if self.asset_1 not in tickers:
            raise ValueError(
                f'Asset {self.asset_1} not in tickers.'
            )

        if  self.asset_2 is not None and self.asset_2 not in tickers:
            raise ValueError(
                f'Asset {self.asset_2} not in tickers.'
            )

        if self.view_type == 'relative' and self.asset_1 == self.asset_2:
            raise ValueError(
                f'Relative views must contain two different assets.'
            )

        row = np.zeros(len(tickers))

        if self.view_type == 'relative':
            row[tickers.index(self.asset_1)] = 1
            row[tickers.index(self.asset_2)] = -1

        else:
            row[tickers.index(self.asset_1)] = 1

        return row

class ViewSet:
    def __init__(self, views):
        self.views = views

    def matrices(self, tickers):
        P = np.vstack([view.p_row(tickers) for view in self.views])
        q = np.array([view.value for view in self.views])

        return P, q

def construct_views(view_args, tickers):
    if not view_args:
        return None, None
    
    views = []

    for view in view_args:
        if view[0] == "relative":
            _, asset_1, asset_2, value = view

            views.append(
                View(
                    view_type="relative",
                    asset_1=asset_1,
                    asset_2=asset_2,
                    value=float(value)
                )
            )

        elif view[0] == "absolute":
            _, asset_1, value = view

            views.append(
                View(
                    view_type="absolute",
                    asset_1=asset_1,
                    value=float(value)
                )
            )

        else:
            raise ValueError(f"Unknown view type: {view[0]}")

    view_set = ViewSet(views)
    return view_set.matrices(tickers)