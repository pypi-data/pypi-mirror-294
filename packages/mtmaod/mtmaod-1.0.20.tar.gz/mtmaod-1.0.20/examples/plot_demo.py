import numpy as np

if __name__ == "__main__":
    x = np.arange(0, 2, 0.01)
    y = np.arange(0, 2, 0.01)

    # Note: if use non-GUI backend, then save_path must be specified
    # from mtmaod import mpl
    # mpl.use("Agg")

    # ====================旧版本====================
    from mtmaod.plot import density_chart

    # save path
    density_chart(x=x, y=y, save_path="demo_scatter.png", type="scatter", bins=25, dpi=300)
    density_chart(x=x, y=y, save_path="demo_pcolormesh.png", type="grid", bins=10, dpi=300, style="single_bold")
    density_chart(x=x, y=y, save_path="demo_kernels.png", type="kernels", dpi=300)

    # # show in GUI
    density_chart(x=x, y=y, type="kernels", dpi=300)

    # ====================新版本====================
    from mtmaod.chart import example_config, plot_default_density_kernel_chart

    print("默认配置", example_config)

    # 使用默认配置绘图
    plot_default_density_kernel_chart(x=x, y=y, save_path="demo_kernels_0.png")

    # 直接传参，覆盖部分默认配置
    plot_default_density_kernel_chart(
        x=x, y=y, save_path="demo_kernels_1.png", figsize=(6, 6), title="Demo", xlabel="X", ylabel="Y"
    )
    # 传入配置，覆盖部分默认配置
    config = example_config.copy()
    config.update({"figsize": (6, 6), "title": "Demo", "xlabel": "X", "ylabel": "Y"})
    plot_default_density_kernel_chart(x=x, y=y, save_path="demo_kernels_2.png", **config)
