from imaaage.pipeline import Preset, SDXLPipeline

default_preset = "tomo-default"

available_presets = {
    "tomo-default": Preset(
        base_model_name="RunDiffusion/Juggernaut-XL-v9",
        performance="极速",
        prompt_style="tomo-default",
        resolution="920×920[0.9]",

    ),

    "normal": Preset(
        base_model_name="RunDiffusion/Juggernaut-XL-v9",
        performance="速度",
        prompt_style="cinematic-default",
        guidance_scale=4.0
    )
}


class Preloader:
    pipes = {}

    @classmethod
    def get(cls, name: str):
        if name not in cls.pipes:
            print(f"cannot find preloaded {name}, use {default_preset}")
        return cls.pipes.get(name, default_preset)

    @classmethod
    def init(cls, *names: str):
        presets = []
        for name in names:
            if name not in available_presets:
                continue
            presets.append(name)

        if len(presets) == 0:
            presets.append(default_preset)

        presets = list(set(presets))

        for preset in presets:
            cls.pipes[default_preset] = SDXLPipeline(preset=available_presets[default_preset])
            print(f"init {preset} OK")
