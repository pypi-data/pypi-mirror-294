from src.imaaage.path import default_lcm_lora

performances = ["极速", "速度", "质量", "自定义"]

default_performance = "速度"


def perform_performance(performance):
    if performance == "速度":
        return dict(
            steps=30,
            switch=24
        )

    elif performance == "极速":
        return dict(
            guidance_scale=1.2,
            lcm_lora=(default_lcm_lora, 1.0),
            sampler="LCM",
            steps=8,
            switch=6
        )

    elif performance == "质量":
        return dict(
            steps=60,
            switch=48
        )

    else:
        return dict()
