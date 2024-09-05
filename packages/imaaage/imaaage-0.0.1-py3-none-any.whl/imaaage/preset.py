from src.imaaage.pipeline import Preset

available_presets = {
    "Tomo默认方案": Preset (
        base_model_name="RunDiffusion/Juggernaut-XL-v9",
        performance="极速",
        prompt_style="tomo-default",
        resolution="920×920[0.9]",

    ),

    "常规方案": Preset(
        base_model_name="RunDiffusion/Juggernaut-XL-v9",
        performance="速度",
        prompt_style="cinematic-default",
        guidance_scale=4.0
    )
}
