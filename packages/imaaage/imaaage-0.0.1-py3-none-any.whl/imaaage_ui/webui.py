import time
import random
import gradio as gr

from src.imaaage.log import current_img_log_file, current_eval_log_file
from src.imaaage.path import models, loras, refiners, default_lora_name, default_base_model_name
from src.imaaage.styles import filter_style, style_categories
from src.imaaage.resolutions import resolutions
from src.imaaage.performance import performances
from src.imaaage.adapters import available_samplers
from src.imaaage.preset import available_presets
from src.imaaage.evaluate import Evaluator, headers

from src.imaaage_ui.executor import Executor
from src.imaaage_ui.html import make_progress_html, css


def generate_clicked(*args):
    yield gr.update(interactive=False), \
          gr.update(visible=True, value=make_progress_html(1, '模型加载中...')), \
          gr.update(visible=True, value=None), \
          gr.update(visible=False)

    future = Executor.submit(*args)
    finished = False

    while not finished:
        time.sleep(0.01)
        if len(Executor.outputs) > 0:
            percentage, title, image = Executor.outputs.pop(0)
            if len(Executor.outputs) > 0:
                continue

            yield gr.update(interactive=False), \
                  gr.update(visible=True, value=make_progress_html(percentage, title)), \
                  gr.update(visible=True, value=image) if image is not None else gr.update(), \
                  gr.update(visible=False)
        finished = future.done()

    yield gr.update(interactive=True), \
          gr.update(visible=False), \
          gr.update(visible=False), \
          gr.update(visible=True, value=future.result())


def evaluate_clicked(test_dataset_selected, test_preset_selected):
    yield gr.update(interactive=False), \
          gr.update(visible=True, value=make_progress_html(1, "加载评估模型...")), \
          gr.update(samples=Evaluator.samples), \
          gr.update()

    future = Evaluator.submit(test_dataset_selected, test_preset_selected)
    finished = False

    while not finished:
        time.sleep(0.1)
        if len(Evaluator.outputs) > 0:
            percentage, title, _ = Evaluator.outputs.pop(0)
            yield gr.update(interactive=False), \
                  gr.update(visible=True, value=make_progress_html(percentage, title)), \
                  gr.update(samples=Evaluator.samples), \
                  gr.update()

        finished = future.done()

    yield gr.update(interactive=True), \
          gr.update(visible=False), \
          gr.update(samples=future.result()), \
          gr.update(value=Evaluator.report())


gradio_root = gr.Blocks(title='Tomo生图', css=css).queue()
with gradio_root:
    with gr.Tab("试验场"):
        with gr.Row():
            with gr.Column(scale=10):
                progress_window = gr.Image(label='预览', show_label=True, height=555,
                                           visible=False, type="pil", interactive=False)
                progress_html = gr.HTML(visible=False, elem_id='progress-bar', elem_classes='progress-bar')
                gallery = gr.Gallery(label='结果', show_label=False, object_fit='contain', height=600, visible=True)
                with gr.Row(elem_classes='type_row'):
                    with gr.Column(scale=85):
                        prompt = gr.Textbox(show_label=False, placeholder="输入正向prompt...",
                                            container=False, autofocus=True, elem_classes='type_row', lines=1024)
                    with gr.Column(scale=15, min_width=0):
                        run_button = gr.Button("生成", elem_classes='type_row')

                with gr.Column():
                    enable_setting = gr.Checkbox(label="启用普通设置", container=False, elem_classes='min_check')
                    enable_advance = gr.Checkbox(label="启用高级参数(不要轻易修改)", container=False, elem_classes='min_check')

            with gr.Column(scale=6) as right_col:
                with gr.Tab(label='预设'):
                    preset_selected = gr.Radio(label="预设方案", info="加载预设方案将会自动配置参数",
                                               choices=list(available_presets.keys()))


                    def apply_preset(selected):
                        preset = available_presets[selected].collate()
                        lora_updates = [
                            gr.update(value='None'), gr.update(value=0.5),
                            gr.update(value='None'), gr.update(value=0.5),
                            gr.update(value='None'), gr.update(value=0.5),
                        ]
                        if preset.lora_model_names is not None:
                            for idx, (lora, weight) in enumerate(loras):
                                print(idx, lora, weight)
                                lora_updates[idx * 2] = gr.update(value=lora)
                                lora_updates[idx * 2 + 1] = gr.update(value=weight)

                        return [gr.update(value=preset.base_model_name),
                                gr.update(value=preset.refiner_model_name),
                                gr.update(value=preset.resolution),
                                gr.update(value=preset.performance),
                                gr.update(value=preset.prompt_style),
                                gr.update(value=preset.guidance_scale),
                                gr.update(value=preset.clip_skip),
                                gr.update(value=preset.switch),
                                gr.update(value=preset.steps),
                                gr.update(value=preset.sampler)] + lora_updates

                with gr.Tab(label='设置', visible=False) as tab_setting:
                    performance_selection = gr.Radio(label='性能', info="不同性能将会预制不同配置，极速使用LCM加速，自定义情况下高级参数才能生效。",
                                                     choices=performances,
                                                     value='速度')
                    resolution_selection = gr.Dropdown(label='分辨率（宽 × 高）',
                                                       info="sdxl采用原始分辨率作为控制信息，分辨率使用傅里叶编码而不是原始尺寸值，所以效果不如预设的分辨率值。",
                                                       choices=list(resolutions.keys()),
                                                       value='1024×1024')
                    image_number = gr.Slider(label='数量', minimum=1, maximum=32, step=1, value=1)
                    negative_prompt = gr.Textbox(label='反向提示词', show_label=True, placeholder="输入负向prompt...")
                    seed_random = gr.Checkbox(label='随机种子', value=True)
                    image_seed = gr.Number(label='种子', value=0, precision=0, visible=False)


                    def random_checked(r):
                        return gr.update(visible=not r)


                    def refresh_seed(r, s):
                        return random.randint(1, 1024 * 1024 * 1024) if r else s


                    seed_random.change(random_checked, inputs=[seed_random], outputs=[image_seed])

                with gr.Tab(label='风格', visible=False) as tab_style:
                    style_filter = gr.Dropdown(label="风格过滤器", choices=style_categories, value="cinematic",
                                               info="通过选定预设的prompt模板，通过文本指令来控制图像风格。")
                    style_selection = gr.Radio(show_label=False, container=True,
                                               choices=filter_style("cinematic"),
                                               value='cinematic-default')


                    def filter_styles(c):
                        return gr.update(choices=filter_style(c))


                    style_filter.change(filter_styles, inputs=[style_filter], outputs=[style_selection])

                with gr.Tab(label="高级参数", visible=False) as tab_advance:
                    with gr.Tab(label="模型"):
                        with gr.Row():
                            base_model = gr.Dropdown(label='SDXL基座模型', choices=list(models.keys()),
                                                     value=default_base_model_name, show_label=True)
                            refiner_model = gr.Dropdown(label='SDXL精炼模型',
                                                        choices=['None'] + list(refiners.keys()),
                                                        value='None', show_label=True)
                        with gr.Accordion(label='LoRA适配器', open=True):
                            lora_ctrls = []
                            for i in range(3):
                                with gr.Row():
                                    lora_model = gr.Dropdown(label=f'SDXL LoRA {i + 1}',
                                                             choices=['None'] + list(loras.keys()),
                                                             value=default_lora_name if i == 0 else 'None')
                                    lora_weight = gr.Slider(label='权重', minimum=-2, maximum=2, step=0.01, value=0.5)
                                    lora_ctrls += [lora_model, lora_weight]
                    with gr.Tab(label="其它"):
                        gr.Markdown("只有在performance=自定义的时候，下面参数才能生效")
                        sampler = gr.Dropdown(label="sampler", choices=available_samplers, value="DPM++ 2M Karras")
                        guidance_scale = gr.Slider(label="guidance scale", value=7.5,
                                                   minimum=0.0, maximum=30.0, step=0.1)
                        clip_skip = gr.Slider(label="clip skip", value=0, minimum=0, maximum=12, step=1)
                        switch = gr.Slider(label="switch", value=24, maximum=100, step=1)
                        steps = gr.Slider(label="steps", value=30, maximum=100, step=1)

                gr.HTML(value=f'<a href="history/{current_img_log_file()}" target="_blank">\U0001F4DA 历史记录</a>')

            enable_advance.change(lambda x: gr.update(visible=x), inputs=[enable_advance], outputs=[tab_advance])
            enable_setting.change(lambda x: gr.update(visible=x), inputs=[enable_setting], outputs=[tab_setting]).then(
                lambda x: gr.update(visible=x), inputs=[enable_setting], outputs=[tab_style])

            preset_ctrls = [base_model, refiner_model, resolution_selection, performance_selection, style_selection,
                            guidance_scale, clip_skip, switch, steps, sampler] + lora_ctrls
            preset_selected.select(apply_preset, inputs=[preset_selected], outputs=preset_ctrls)
            ctrls = [prompt, negative_prompt, style_selection,
                     performance_selection, resolution_selection, image_number, image_seed] + \
                    [base_model, refiner_model] + \
                    [sampler, guidance_scale, clip_skip, switch, steps] + lora_ctrls

            run_button.click(fn=refresh_seed, inputs=[seed_random, image_seed], outputs=image_seed) \
                .then(fn=generate_clicked, inputs=ctrls, outputs=[run_button, progress_html, progress_window, gallery])
    with gr.Tab("评估"):
        with gr.Row():
            with gr.Column(scale=10):
                test_result = gr.Textbox(label="评估结果", container=False, lines=24, interactive=False)
                test_progress = gr.HTML(visible=False, elem_id='progress-bar', elem_classes='progress-bar')
                run_test = gr.Button("开始评估")

            with gr.Column(scale=6):
                test_dataset_selection = gr.Dropdown(label="测试集", choices=["默认"])
                test_preset_selection = gr.Dropdown(label="待评估预设", choices=list(available_presets.keys()))

                gr.HTML(value=f'<a href="history/{current_eval_log_file()}" target="_blank">📝 评估记录</a>')

        test_cases = gr.Dataset(
            label="测试集",
            headers=headers,
            components=[gr.Number(visible=False), gr.Textbox(visible=False), gr.Textbox(visible=False),
                        gr.Image(visible=False), gr.Number(visible=False), gr.Number(visible=False)])


        def preview_cases(evt: gr.SelectData):
            return gr.update(samples=Evaluator.preview(evt.value))


        test_dataset_selection.select(preview_cases, inputs=None, outputs=[test_cases])
        run_test.click(evaluate_clicked, inputs=[test_dataset_selection, test_preset_selection],
                       outputs=[run_test, test_progress, test_cases, test_result])
