import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['agg.path.chunksize'] = 10**10


class MatplotFig:

    @staticmethod
    def time_series_data(x, **kwargs):
        """ Plot 1d data

        Args:
            x (array): shape:=(N,)
            show (bool): opt. default True
            save (bool): opt. default False
            savepath (string): opt. default './plot.jpg'
            ylim (list): opt. [low, up]
            title (string): opt.
            xlabel (string): opt.
            ylabel (string): opt.

            sr (int / float): opt. sampling rate 

        Returns:
            None
        """
        _show = kwargs.get('show', True)
        _save = kwargs.get('save', False)
        _savepath = kwargs.get('savepath', './fig.jpg')
        _ylim = kwargs.get('ylim')
        _title = kwargs.get('title')
        _xlabel = kwargs.get('xlabel')
        _ylabel = kwargs.get('ylabel')

        _sr = kwargs.get('sr')

        # Plot
        fig, ax = plt.subplots()
        ax.set_ylim(_ylim)
        ax.set_title(_title)
        ax.set_xlabel(_xlabel)
        ax.set_ylabel(_ylabel)
        ax.grid()

        if not _sr:
            ax.plot(x)

        else:
            data_len = len(x)
            tmp = np.linspace(0, data_len, data_len)
            time = tmp / _sr
            ax.plot(time, x)

        if _show:
            plt.show()
        if _save:
            plt.savefig(_savepath)
        return None

    @staticmethod
    def clusters(x, y, labels, classes, **kwargs):
        """Scatter plot the 2d data with discrete classes

        Args:
            x (array): (N,)
            y (array): (N,)
            labels (array): (N,)
            classes (str list): [type1, type2..]
            show (bool): opt. default True
            save (bool): opt. default False
            savepath (string): opt. default './plot.jpg'
            title (string): opt.
            xlabel (string): opt.
            ylabel (string): opt.
            size (int): opt. marker size
            alpha (float): opt. marker transparency
            cmap: opt. plt.cm.plasma

        Returns:
            None
        """
        _show = kwargs.get('show', True)
        _save = kwargs.get('save', False)
        _savepath = kwargs.get('savepath', './plot.jpg')
        _title = kwargs.get('title')
        _xlabel = kwargs.get('xlabel')
        _ylabel = kwargs.get('ylabel')
        _size = kwargs.get('size')
        _alpha = kwargs.get('alpha')
        _cmap = kwargs.get('cmap', plt.cm.plasma)  # plasma Pastel1

        _yticklabels = classes

        # Plot
        fig, ax = plt.subplots()
        n_label = len(_yticklabels)
        bounds = np.linspace(0, n_label, n_label+1)
        ticks = np.linspace(0.5, n_label-0.5, n_label)
        norm = mpl.colors.BoundaryNorm(bounds, _cmap.N)
        img = ax.scatter(x,
                         y,
                         c=labels,
                         s=_size,  # marker size
                         alpha=_alpha,  # transparency
                         cmap=_cmap,
                         norm=norm)
        label = [int(i) for i in labels]
        cb = plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=_cmap),
                          ticks=ticks,)
        cb.ax.set_yticklabels(_yticklabels)
        plt.title(_title)
        plt.xlabel(_xlabel)
        plt.ylabel(_ylabel)

        if _show:
            plt.show()
        if _save:
            # fig = plt.gcf()
            # fig.set_size_inches(16, 9)
            # fig.savefig(f'_plot.png', dpi=100)
            plt.savefig(_savepath)
        return None
