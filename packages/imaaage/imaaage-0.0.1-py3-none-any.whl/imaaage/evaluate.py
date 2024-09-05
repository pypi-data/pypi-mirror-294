import time
import copy
import uuid
import numpy as np
from PIL import Image

from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

from src.imaaage.log import log_evaluation, pretty_eval_report, log_img
from src.imaaage.metric import ImageEvaluator
from src.imaaage.pipeline import Payload, SDXLPipeline, Preset
from src.imaaage.preset import available_presets

case_default = [
    ['''not found''',
     '''A energetic young woman in workout clothes, slightly sweaty but smiling, giving a thumbs up after a crossfit session. She is standing in the foreground of a crossfit gym. The background shows crossfit equipment including barbells, weight plates, and pull-up bars. The woman has a determined and satisfied expression, her hair is slightly messy from the workout, and there's a slight sheen of sweat on her skin. The lighting is bright and energetic, emphasizing the positive atmosphere of the gym.'''],

    ['''not found''',
     '''A vibrant and energetic image of a young college student who has just finished a CrossFit workout. The student is wearing colorful workout clothes - a bright blue tank top and black shorts. They are visibly sweaty, with a glistening forehead and damp hair, but have a big, triumphant smile on their face. The student is giving an enthusiastic thumbs up with one hand, while the other hand is resting on their hip. Their posture exudes confidence and accomplishment. In the background, you can see various CrossFit equipment: a rack of barbells to the left, colorful kettlebells of different sizes on the right, and a pull-up bar visible above. The lighting is bright and energetic, emphasizing the student's enthusiasm and the dynamic atmosphere of the CrossFit gym. The overall color palette is vibrant, with pops of red, blue, and yellow to convey energy and excitement.'''],

    ['''not found''',
     '''A young, energetic person in workout clothes standing in a CrossFit gym. The person looks tired but happy, with a slight sheen of sweat on their skin. They're holding a water bottle in one hand and have a white towel draped around their neck. The background shows a typical CrossFit gym environment with various equipment visible, such as barbells, kettlebells, medicine balls, and pull-up bars. The lighting is bright and energetic, highlighting the determination in the person's eyes and the modern, industrial feel of the gym.'''],

    ['''not found''',
     '''A young, energetic college student after a CrossFit session. The student looks tired but happy, with a beaming smile and slightly sweaty face. They are wearing colorful workout clothes - a fitted t-shirt and shorts. The student is holding a water bottle in one hand and giving a thumbs up with the other. The background shows a modern gym setting with CrossFit equipment like barbells, kettlebells, and pull-up bars visible. The lighting is bright and energetic, emphasizing the positive atmosphere.'''],

    ['''not found''',
     '''A tired but happy person after a CrossFit workout. The individual is standing in a gym setting, wearing workout clothes - a sweat-soaked gray tank top and black shorts. Their skin is glistening with sweat, and they have a satisfied smile on their face. The person's hair is slightly messy, and they're holding a water bottle in one hand. In the background, you can see various CrossFit equipment such as barbells, kettlebells, medicine balls, and a pull-up bar. The gym has a rugged, industrial look with concrete floors and exposed brick walls. The lighting is bright but not harsh, creating a motivating atmosphere.'''],

    ['''not found''',
     '''A vibrant indoor badminton court scene with two players in action. The court has clear white lines on a polished wooden floor. In the foreground, one player is mid-jump, arm extended high, racket connecting with the shuttlecock, sending it over the net. This player wears a blue and white sports outfit. On the other side of the net, the second player is in a ready stance, knees bent, racket held in front, preparing to return the shot. This player is dressed in red and white. The net is clearly visible, stretching across the center of the court. Badminton rackets are sleek and modern. The background shows typical indoor court features: high ceilings with bright overhead lights, maybe some spectator seating in the distance. The overall scene is dynamic and energetic, capturing the intensity of the game.'''],

    ['''not found''',
     '''A young woman in workout clothes standing in a gym after a crossfit session. She looks tired but happy, with a slight sheen of sweat on her skin. She's holding a water bottle in one hand and has a white towel draped around her neck. Her hair is slightly messy from the workout. In the background, you can see various crossfit equipment such as barbells, kettlebells, and a pull-up bar. The gym has a modern, industrial feel with concrete floors and motivational posters on the walls. The lighting is bright and energetic.'''],

    ['''not found''',
     '''A high-definition image of a person performing a deadlift in a gym. The subject, who could be a man or woman with an athletic build, is in the center of the frame, gripping a heavy barbell loaded with weight plates. Their posture shows proper deadlift form: feet shoulder-width apart, back straight, chest up, and arms fully extended. The person's face displays intense concentration and determination. The barbell is clearly visible with multiple weight plates on each end. In the background, you can see various gym equipment such as weight racks, benches, and other exercise machines. The lighting is bright but not harsh, highlighting the subject's muscular definition and the sheen of the metal weights. The gym floor is visible, possibly made of rubber matting typical in weightlifting areas.'''],

    ['''not found''',
     '''A person performing a deadlift exercise in a well-equipped gym. The person, wearing shorts and a t-shirt, is gripping a heavy barbell loaded with weight plates. Their posture shows proper form for a deadlift, with legs bent, back straight, and arms fully extended. In the background, various weightlifting equipment is visible, including racks of dumbbells, stacked weight plates of different sizes, and workout benches. The gym has a modern, clean appearance with good lighting, emphasizing the intensity and focus of the weightlifter.'''],

    ['''not found''',
     '''A person lifting weights in a well-equipped gym. The image shows a muscular individual wearing shorts and a t-shirt, performing a barbell lift. The gym background is filled with various weightlifting equipment, including racks of dumbbells, weight plates, and other exercise machines. The lighting is bright and energetic, highlighting the determination on the person's face and the sheen of sweat on their skin. The overall atmosphere is one of strength, dedication, and fitness.'''],

    ['''not found''',
     '''A calendar page showing yesterday's date prominently circled in red. Next to the circled date, there's a small black dumbbell icon. The calendar is white with black text and lines. The rest of the dates are visible but not highlighted. The calendar takes up most of the image, with clean and crisp lines.'''],

    ['''not found''',
     '''A split image with two contrasting scenes. On the left side, a person is lifting weights in a gym setting, wearing workout clothes (shorts and a t-shirt). They are mid-lift, showing effort and strength. On the right side, the same person is running outdoors in a park or nature trail, also wearing workout clothes (shorts and a t-shirt). The runner is in mid-stride, looking energetic and determined. The background on the left should show gym equipment, while the right side should show trees and a path. The image should have a clear divide down the middle, separating the two scenes but showing they are connected. Use vibrant, motivating colors.'''],

    ['''not found''',
     '''A split image with two halves. On the left half, a person wearing workout clothes (shorts and a t-shirt) is lifting weights, showing muscular effort. On the right half, the same person is doing cardio exercise on a treadmill, running with determination. Both scenes are set in a modern gym environment with equipment visible in the background. The lighting is bright and energetic, emphasizing the vigorous nature of the exercises. The split is clean and clear, dividing the image equally.'''],

    ['''not found''',
     '''A side-by-side comparison image of a person's body transformation through weightlifting. On the left side, show a slim person with little muscle definition wearing a light gray t-shirt and navy blue shorts. They have a neutral expression and are standing in a relaxed pose. On the right side, show the same person with significantly more muscle definition, broader shoulders, more defined arms, chest, and legs. They're wearing the same light gray t-shirt and navy blue shorts, but the clothes fit more snugly due to increased muscle mass. The person on the right has a confident smile and is standing in a more powerful pose, slightly flexing to show off their new muscle definition. Both figures are set against a plain white background with a vertical line separating the two images. Above the left figure, add text that says "Before" and above the right figure, add text that says "After". Use a realistic art style to clearly show the muscle development.'''],

    ['''not found''',
     '''A split-screen image. On the left side: A sad young person with downcast eyes and slumped shoulders, representing being bullied. The background is muted and gloomy, with soft, desaturated colors. On the right side: The same person, now older and more confident, lifting weights in a bright gym. Their posture is straight, with a determined expression. The right side uses vibrant, energetic colors. The transition between the two sides is clear but smooth. The overall composition should convey a journey from vulnerability to strength.'''],

    ['''not found''',
     '''A vibrant and inclusive gym scene with people of various body types working out together. The image shows a diverse group of individuals, including men and women of different ages, sizes, and ethnicities, engaged in various exercises. In the foreground, a muscular person is spotting someone lifting weights, offering encouragement. Nearby, an older adult is being assisted by a trainer on an exercise machine. In the background, you can see a mix of cardio equipment like treadmills and ellipticals, as well as weight machines and free weights. The gym is well-lit with motivational posters on the walls. The overall atmosphere is positive and supportive, with people smiling and helping each other. The color palette is warm and inviting, with shades of blue, green, and orange to create an energizing environment.'''],

    ['''not found''',
     '''Split image composition. On the left: A young person looking sad and insecure, hunched over, wearing casual clothes like jeans and a t-shirt, with slumped shoulders and a downcast expression. On the right: The same person, now older and more muscular, standing tall with excellent posture, wearing similar casual clothes that now fit more snugly, exuding confidence with a bright smile and assertive body language. The background transitions from darker, muted colors on the left to brighter, more vibrant colors on the right, symbolizing the positive transformation. 1x1 aspect ratio.'''],

    ['''not found''',
     '''A wide-angle view of a modern gym interior with four clearly labeled weightlifting stations. 1) In the foreground, a muscular person lying on a bench press, lifting a barbell, labeled "Bench Press". 2) To the left, a person performing squats with a heavy barbell on their shoulders, labeled "Squats". 3) In the background center, a person bending forward doing deadlifts with a loaded barbell, labeled "Deadlifts". 4) To the right, a person standing and doing bicep curls with dumbbells, labeled "Bicep Curls". The gym has a clean, well-lit atmosphere with mirrors on the walls, rubberized flooring, and additional weight equipment visible in the background. Use vibrant, energetic colors to convey an active gym environment.'''],

    ['''not found''',
     '''A detailed, high-quality image of a person performing a deadlift exercise with perfect form. The person is facing sideways to clearly show the technique. They have feet shoulder-width apart, knees slightly bent, and are gripping a heavy barbell. The back is straight, chest up, and they're in the process of standing up straight while lifting the barbell. The background is a clean, well-lit gym setting. The image should emphasize proper posture and muscle engagement, showcasing the full-body nature of the exercise.'''],

    ['''not found''',
     '''A person performing a bench press exercise in a gym setting. The image shows a muscular individual lying on a flat bench with their back firmly pressed against it. Their feet are planted on the ground for stability. The person's arms are fully extended, holding a heavy barbell directly above their chest. The proper form is clearly visible: shoulders are retracted, wrists are straight, and the barbell is aligned with the middle of the chest. The background shows other gym equipment, emphasizing the weightlifting environment. The lighting is bright and even, highlighting the person's form and muscle definition.'''],

    ['''not found''',
     '''A realistic image of a person standing in front of a gym equipment rack, looking thoughtful. The person is wearing workout clothes and has a contemplative expression. The equipment rack is filled with various items including dumbbells of different sizes, a coiled jump rope, colorful resistance bands, and a rolled-up yoga mat. The background suggests a gym setting with neutral colors. Above the person's head is a large, clear speech bubble containing the text "Yesterday, I _ at the gym." with a blank space for filling in an exercise. The overall composition should be balanced, with the person slightly to one side and the equipment rack taking up a significant portion of the image.'''],

    ['''not found''',
     '''A detailed image of a person performing a bench press in a gym setting. The person is lying on a flat bench with their back firmly pressed against it. Their feet are planted on the ground for stability. The person's arms are fully extended, holding a barbell directly above their chest. The barbell is loaded with weight plates on both ends. A spotter is standing nearby, hands hovering close to the barbell, ready to assist if needed. The scene shows proper bench press form and safety measures. The gym background includes other exercise equipment and mirrors.'''],

    ['''not found''',
     '''A detailed, high-definition image of a person performing a bench press exercise in a gym setting. The person is lying on their back on a flat bench with a determined expression. Their hands are gripping a silver barbell slightly wider than shoulder-width apart. The barbell is lowered to chest level, showing the person at the bottom of the movement. Their legs are planted firmly on the ground, with feet flat on the floor. The person is wearing athletic clothing - a fitted t-shirt and shorts. The background shows gym equipment and mirrors, creating a realistic workout environment. The lighting is bright and even, highlighting the proper form and muscle engagement during the exercise.'''],

    ['''not found''',
     '''A simple, clear diagram of a bench press setup. The image shows two stick figures. One stick figure is lying on a bench with arms extended upwards, holding a barbell. This figure is labeled "Lifter" in clear text. Next to the bench, another stick figure is standing, labeled "Spotter" in clear text. The bench and barbell are drawn with bold, easy-to-see lines. At the top of the image, there's a title that says "Bench Press Setup" in large, clear letters. The background is white for maximum clarity. The style is minimalist and easy to understand, like a clear instructional diagram.'''],

    ['''not found''',
     '''A cheerful college-age teacher in workout clothes after a CrossFit session. The person is in their early 20s, with a fit physique, wearing colorful athletic wear such as a bright tank top and fitted workout shorts. Their hair is slightly messy and damp with sweat. They have a tired but genuinely happy expression, with a wide smile and bright eyes. There's a towel draped around their neck. The background shows a modern gym or fitness center with CrossFit equipment like barbells, kettlebells, and pull-up bars visible. The lighting is warm and energetic, reflecting the positive atmosphere of the gym.'''],

    ['''not found''',
     '''A young, energetic college student in workout clothes, looking slightly sweaty but happy after a CrossFit session. The student is smiling broadly, with a towel around their neck and a water bottle in hand. They are standing in the foreground of a CrossFit gym. The background shows various CrossFit equipment such as barbells, kettlebells, pull-up bars, and rowing machines. The lighting is bright and energetic, highlighting the student's enthusiasm and the gym's dynamic atmosphere. The color palette includes vibrant blues, reds, and grays typical of a modern gym setting.'''],

    ['''not found''',
     '''A vibrant badminton court scene with two players in action. One player is mid-swing, hitting a shuttlecock (birdie) over the net. The other player is positioned ready to receive. Both players are holding badminton rackets clearly visible in their hands. The badminton net is prominently displayed in the center of the image, dividing the court. The court lines are visible on a light-colored surface. The players are wearing colorful sports attire. The scene is well-lit, showcasing the dynamic movement and energy of the game.'''],

    ['''not found''',
     '''A detailed image of a calendar hanging on a wall, with several recent dates circled or marked in red. In the bottom right corner of the image, there's a badminton racket leaning against the wall with a shuttlecock next to it. The calendar should be the main focus, taking up about 70% of the image, while the badminton equipment occupies the remaining 30% in the corner. The calendar should have a clean, modern design with clearly visible dates and month. The circled dates should stand out against the white background of the calendar.'''],

    ['''not found''',
     '''A calendar page showing the current month, with last weekend's dates highlighted in yellow. In the bottom right corner, there's a small image of a badminton racket and shuttlecock. The calendar should be the main focus, taking up about 80% of the image, while the badminton equipment is smaller and placed in the corner. The calendar should have a clean, modern design with clear numbers and day names. The badminton racket should be sleek and professional-looking, with the shuttlecock positioned nearby as if in mid-flight.'''],

    ['''not found''',
     '''A vibrant, sunny outdoor scene of a badminton court with 4 friends playing an exciting game. The image shows 2 players on each side of the net, caught in mid-action with rackets raised. They are all smiling and clearly having fun. The court is visible with clear boundary lines, and a sturdy net stretches across the middle. Shuttlecocks can be seen in the air. The players are wearing colorful, sporty attire suitable for badminton. The background shows a clear blue sky with a few fluffy white clouds, and some trees or bushes around the court to give a sense of an outdoor setting. The lighting is bright and cheerful, highlighting the fun and energetic atmosphere of the game.'''],

    ['''not found''',
     '''A split-screen image of a professional badminton player's day. On the left side, show the player practicing in a gym with a coach. The player is in mid-motion, hitting a shuttlecock with their racket while the coach observes and gives instructions. The gym has bright lighting and several badminton courts visible in the background. On the right side, show the same player competing in a professional match. The player is leaping high to smash a shuttlecock, with their racket raised above their head. The competition court is surrounded by spectators and has official tournament banners. In both scenes, the player wears professional badminton attire in vibrant colors. The shuttlecock is clearly visible in mid-air in both scenes. The image should have a dynamic, energetic feel with sharp details and bright colors.'''],

    ['''not found''',
     '''An indoor badminton court at night. A player in mid-action, hitting a shuttlecock with a racket. The court is well-lit, but the surrounding areas are dimmer, suggesting it's evening. The badminton net is clearly visible, dividing the court. White court lines are marked on the floor. In the background, there are some gym equipment like weight racks and exercise balls. The player is wearing sports attire and is captured in a dynamic pose, demonstrating perfect form. The shuttlecock is visible in mid-air. The overall atmosphere is energetic and focused.'''],

    ['''not found''',
     '''A vibrant badminton court scene with two players in action. One player, representing the student, is lunging forward with their racket extended, about to hit a shuttlecock in mid-air. The other player is on the opposite side of the net, poised and ready to receive. Both players are wearing colorful sports attire. The court is well-lit with clear boundary lines. The net is taut across the center of the court. In the background, you can see other courts and spectators. The scene captures the energy and excitement of a badminton match.'''],

    ['''not found''',
     '''A vibrant, sunny outdoor scene of 3-4 diverse friends playing badminton together. The players are smiling and laughing, clearly enjoying a casual game. Two players are positioned on either side of a badminton net, with rackets raised mid-swing. A shuttlecock is visible in the air between them. The background shows a park or backyard setting with some trees and grass. The players are dressed in casual, colorful sportswear. The overall atmosphere is cheerful and energetic, capturing the fun of friendly competition.'''],

    ['''not found''',
     '''A lively scene of 3-4 friends playing badminton on a court. The players are in dynamic poses, showcasing an energetic game in progress. Shuttlecocks are visible in the air. The players have bright smiles on their faces, expressing joy and excitement. In the corner of the image, there's a clock or watch showing 2:00, indicating that 2 hours have passed. The overall atmosphere is vibrant and fun, with the court and surrounding area visible in the background.'''],

    ['''not found''',
     '''Split-screen image. On the left side: A person examining a badminton racket closely, holding it up to their face, inspecting the strings and frame with a focused expression. The background is a badminton court. On the right side: A group of four friends celebrating after winning a game on a badminton court. They are jumping with joy, high-fiving each other. One person in the center (representing the student) is holding up a shuttlecock triumphantly above their head with a big smile. The two halves of the image are separated by a clear vertical line down the middle.'''],

    ['''not found''',
     '''A serene and tranquil park scene with a wooden bench in the foreground. The park is lush with green grass and scattered with colorful flowers. Tall, leafy trees provide shade and frame the scene. A winding path leads through the park, disappearing into the distance. Soft, warm sunlight filters through the leaves, creating a dappled effect on the ground. The atmosphere is peaceful and inviting, perfect for relaxation and contemplation. The image should have a soft, dreamy quality with pastel colors to evoke a sense of calm and tranquility.'''],

    ['''not found''',
     '''A simple, clean illustration of a badminton racket and shuttlecock in the bottom right corner of a white background. The racket and shuttlecock should be small, occupying about 15% of the image. The racket should be at a slight angle, with the shuttlecock above it as if in mid-flight. Use bold, clear lines and minimal detail to ensure visibility when scaled down.'''],

    ['''not found''',
     '''A top-down view of a badminton court with clear, labeled elements. The court should have distinct white lines on a light green surface. Label the net across the center, court lines including sidelines and baselines, serving areas on both sides, and out-of-bounds areas. Include a realistic badminton racket and shuttlecock placed near one corner of the court. The image should be clean, informative, and visually appealing, suitable for an educational presentation.'''],

    ['''not found''',
     '''A young woman in her early 20s performing a kettlebell swing in a well-equipped gym. She's wearing a colorful tank top and black leggings. Her face shows a determined expression, showcasing the intensity of the workout. The background includes other gym equipment like barbells, pull-up bars, and medicine balls. The overall color scheme is energetic with bright, vibrant colors. The image should be high-definition, showcasing the dynamic movement of the kettlebell swing and the details of the gym environment.'''],

    ['''not found''',
     '''A young, energetic woman in workout clothes standing in a gym after a crossfit session. She looks tired but happy, with a big smile on her face and giving a thumbs up. Her hair is slightly messy and she has a light sheen of sweat. In the background, you can see various exercise equipment such as barbells, kettlebells, and a pull-up bar. The lighting is bright and energetic, highlighting her accomplishment. The color palette is dominated by cool gym tones with pops of color from the equipment.'''],

    ['''not found''',
     '''A vibrant, high-definition image of a person running on a scenic trail. The runner, in mid-stride, wears comfortable running clothes - a breathable, bright blue t-shirt and black running shorts. They have on high-quality running shoes in white and orange. The runner's face shows an expression of joy and determination. The background is a lush, green forest with sunlight filtering through the trees, creating dappled light on the dirt trail. In the distance, you can see a small clearing with wildflowers. The overall scene conveys a sense of freedom, health, and connection with nature.'''],

    ['''not found''',
     '''A vivid, detailed image of an ancient Greek runner in a white toga, sprinting along a dusty dirt path. The runner is muscular and athletic, with a determined expression. In the background, majestic ancient Greek buildings are visible, including columned temples and stone structures. The scene has a warm, golden light, giving it a historical and timeless feel. The sky is a soft blue with wispy clouds. The overall composition should evoke the spirit of ancient Olympic games and Greek civilization.'''],

    ['''not found''',
     '''A flat lay composition of modern running gear against a plain white background. The items are neatly arranged and include: 1) A pair of sleek, brightly colored running shoes with mesh uppers and cushioned soles. 2) A pair of lightweight, breathable running shorts in a dark color. 3) A moisture-wicking t-shirt in a vibrant color, made of technical fabric with a slight sheen. 4) A modern sports watch with a large digital display, showing fitness tracking features. The items are evenly spaced and well-lit, creating a clean and appealing composition that showcases the essential gear for a modern runner.'''],

    ['''not found''',
     '''A flat lay photograph of essential running gear neatly arranged on a light gray background. The image includes a pair of modern running shoes with vibrant colors, positioned in the center. To the left, there's a pair of black running shorts folded neatly. On the right, a bright moisture-wicking t-shirt is laid out flat. Above the shoes, there's a sleek water bottle. Below the shoes, a colorful headband is placed. The items are arranged in a visually pleasing composition, with soft shadows to give depth. The image has a clean, motivational feel, perfect for inspiring runners.'''],

    ['''not found''',
     '''A young, energetic person doing a CrossFit workout in a gym setting. The individual is lifting a heavy barbell, mid-movement in a clean and jerk exercise. Their muscles are visibly tense, with sweat glistening on their skin. The person's face shows a mix of intense concentration and a hint of a smile, indicating they're tired but happy. The background shows typical CrossFit equipment like kettlebells, jump ropes, and pull-up bars. The lighting is bright and energetic, emphasizing the intensity of the workout. The color palette is dominated by cool grays of the gym equipment, contrasted with the warm skin tones of the athlete and perhaps some bright colors from gym mats or wall decorations.'''],

    ['''not found''',
     '''A vibrant image featuring a close-up of an orange basketball in the foreground, showing clear details of its pebbled texture and black lines. The basketball takes up about a third of the image on the bottom right. In the background, there's a partial view of a basketball court with visible white court lines on a polished wooden floor. On the left side of the image, a basketball hoop with a white net is visible. The lighting is bright and even, highlighting the contrast between the orange basketball and the warm tones of the wooden court floor. The image has a 1:1 aspect ratio.'''],

    ['''not found''',
     '''A cheerful and welcoming image with the text "Hello! Let's chat!" in the center. The text should be in a friendly, colorful font with a mix of bright colors like blue, green, yellow, and pink. The background is light pastel yellow, creating a warm and inviting atmosphere. Around the text, there are simple, cartoon-style speech bubbles in various sizes and pastel colors (light blue, light green, and light pink). In the corners of the image, add small conversation icons like a smiling face, a hand waving, and a thumbs-up gesture. The overall style should be simple, clean, and appealing, suitable for a friendly chat invitation.'''],

    ['''not found''',
     '''A nighttime scene of an outdoor basketball court lit by warm, glowing street lamps. Silhouettes of a group of friends playing basketball are visible against the dark night sky. One player is in mid-air, shooting the ball towards the hoop. The court is surrounded by trees and urban buildings in the background. The atmosphere is energetic and fun, with dynamic poses of the players. The warm light creates a contrast with the cool night sky, highlighting the players' movements and the ball's trajectory. The scene captures the excitement and camaraderie of a night game among friends.'''],

    ['''not found''',
     '''A nighttime outdoor basketball scene with two silhouetted friends playing. The basketball court is dimly lit, with a bright full moon in the sky and a few street lamps casting a warm glow. The two players are in mid-action, their dark silhouettes contrasting against the night sky. A basketball is visible in mid-air between the two players, creating a dynamic scene. The atmosphere is casual and friendly, conveying the sense of a fun night game between friends. The court lines are faintly visible, and there might be some trees or urban buildings in the background to set the scene.'''],

    ['''not found''',
     '''A nighttime scene of a group of friends playing basketball on an outdoor court. The court is illuminated by warm, glowing streetlights and floodlights, creating a vibrant atmosphere against the dark sky. In the foreground, one player is mid-jump, about to shoot the ball towards the hoop. Two defenders have their arms raised, trying to block the shot. On the sides, two more players are positioned, ready to catch a potential rebound. The players are diverse in appearance, wearing colorful basketball jerseys and shorts. Their faces show determination and excitement. The basketball court lines are clearly visible, reflecting the bright lights. In the background, you can see some trees and urban buildings silhouetted against the night sky. The overall scene captures the energy, friendship, and fun of a nighttime basketball game.'''],

    ['''not found''',
     '''A bright, sunny summer day scene. In the clear blue sky, there's a large, cartoonish smiling sun with rays emanating from it. The landscape below features several trees with full, lush green leaves. In the foreground, there's a person wiping their forehead with the back of their hand, indicating it's hot. The overall color palette is vibrant and cheerful, with warm yellows, bright greens, and sky blues dominating the scene. The style is slightly cartoonish and friendly, perfect for a presentation slide. At the bottom of the image, there's space for text to be added later.'''],

    ['''not found''',
     '''A split-screen image divided vertically. On the left side, a vibrant basketball court scene with players in action, featuring bright orange basketballs and players in colorful jerseys. The court has clear white lines and a shiny wooden floor. On the right side, a large, bold blue question mark centered against a light background, surrounded by various food items such as sandwiches, wraps, salads, and different types of bread and fillings. The food items should be colorful and diverse, representing different cuisines. The contrast between the two sides should be striking, with the left side dominated by oranges and browns of the basketball court, and the right side featuring a variety of colors from the different foods. A clear vertical line separates the two halves of the image.'''],

    ['''not found''',
     '''A simple, clean image with a white background. In the center, written in a large, easy-to-read black sans-serif font, is the text "I played basketball..." followed by a blank space, as if inviting completion. To the left of the text, there's a small, orange basketball icon. The overall design is minimalist and clear, perfect for a presentation slide.'''],

    ['''not found''',
     '''A vibrant and energetic basketball game scene on a court. Two players in action: one player dribbling the ball with determination, while the other player is in a defensive stance trying to block. The basketball hoop is visible in the background. The court floor has a shiny wooden texture. The players are wearing brightly colored jerseys - one in red and one in blue. Their expressions show intense focus and athleticism. The lighting is bright, casting dynamic shadows on the court. The scene captures the motion and excitement of the game.'''],

    ['''not found''',
     '''A simple, friendly image with the text "Let's Talk About Basketball!" in a clear, engaging font. The text is centered and prominently displayed. Next to the text, there's a small cartoon-style basketball. The basketball should be recognizable but not too detailed, with its characteristic orange color and black lines. The background is a cheerful, soft pastel color that's easy on the eyes, like a light sky blue or gentle yellow. The overall style is welcoming and fun, perfect for introducing a discussion about basketball.'''],

    ['''not found''',
     '''A simple, cheerful image with the text "Hello! I'm here. Let's chat!" in a large, friendly, easy-to-read font. The text is centrally placed on a light pastel background. Next to the text, there's a cute, simple cartoon character with a big smile, waving its hand in a welcoming gesture. The character has a round face, big eyes, and a cheerful expression. The overall style is clean, modern, and inviting, perfect for a welcoming message.'''],

    ['''not found''',
     '''A dynamic, high-energy image of Michael Jordan in his prime, wearing his iconic red Chicago Bulls jersey with the number 23 clearly visible. Jordan is captured mid-air, soaring towards the basketball hoop for a powerful slam dunk. His muscular arms are extended, holding the basketball with one hand, ready to slam it through the hoop. Jordan's face shows intense concentration and determination. In the background, you can see a glimpse of a packed stadium with fans on their feet, cheering wildly. The lighting dramatically highlights Jordan's figure, creating a sense of heroic action. The scene conveys the excitement and athleticism of professional basketball at its highest level.'''],

    ['''not found''',
     '''A dynamic, high-resolution image of Michael Jordan in his iconic flying dunk pose. Jordan is wearing his red Chicago Bulls uniform with the number 23. He's leaping high in the air towards a basketball hoop, his body fully extended horizontally. His right arm is stretched out in front of him, holding a basketball, ready to slam dunk it. His left arm is slightly bent and trailing behind him. Jordan's face shows intense concentration and determination. The background shows a blurred basketball court with cheering crowds in the stands. The lighting dramatically highlights Jordan's muscular form and the sheen of his uniform. At the top of the image, stylized text reads "Michael Jordan: The Flying Man" in a bold, eye-catching font that complements the action of the scene.'''],

    ['''not found''',
     '''A friendly and reassuring cartoon image with a large, cheerful text saying "I'm here and listening!" in a bold, rounded font. The text is placed prominently in the center of the image, using vibrant blue color. Next to the text, there's a smiling cartoon character representing a teacher or tutor. The character has a kind face, glasses, and is wearing professional but approachable attire like a sweater or button-up shirt. The character has a speech bubble next to them, emphasizing active communication. The background is a soft, warm pastel color like light yellow or peach to create a comforting atmosphere. The overall style is simple, clean, and inviting, perfect for educational or supportive contexts.'''],

    ['''not found''',
     '''A cheerful young woman in colorful workout clothes, smiling broadly and giving a thumbs up after a CrossFit session. She has a slight sheen of sweat on her skin, looking energetic and accomplished. The background is a CrossFit gym with various equipment visible, including barbells, kettlebells, and pull-up bars. The lighting is bright and energizing, highlighting the woman's enthusiasm and the gym's atmosphere. The image should convey a sense of achievement and post-workout excitement.'''],

    ['''not found''',
     '''A smiling, slightly sweaty person in workout clothes, presumably a teacher, giving a thumbs up after a crossfit session. The person looks tired but happy, with a genuine smile and a proud expression. They are wearing form-fitting athletic wear, such as a moisture-wicking t-shirt and shorts. Beads of sweat are visible on their forehead and arms. The background shows a crossfit gym setting with various equipment visible, including a rack of dumbbells, kettlebells, and a prominent pull-up bar. The lighting is bright and energetic, emphasizing the positive mood of the scene. The color palette includes vibrant blues, reds, and grays typical of a modern gym environment.'''],

    ['''not found''',
     '''A swimming pool with clear blue water and visible lane dividers. A person is swimming freestyle stroke in one of the lanes, their arms extended and head turned to breathe. On the poolside, there's a pair of swimming goggles and a bright swimming cap. The pool is indoors with ambient lighting reflecting off the water surface. The scene is vibrant and energetic, capturing the essence of competitive swimming.'''],

    ['''not found''',
     '''A simple, clear illustration of a swimming pool from a top-down view. The pool is rectangular with blue water. Include 3 swim lanes marked with white lines. On one end of the pool, there's a diving board extending over the water. Near one corner, place a tall lifeguard chair. Label the following elements with simple, readable text: 'pool' (pointing to the entire structure), 'water' (pointing to the blue area), 'lane' (pointing to one of the swim lanes), 'diving board' (pointing to the diving board), and 'lifeguard chair' (pointing to the chair). The style should be clean, minimalistic, and easy to understand, with a white background.'''],

    ['''not found''',
     '''A person relaxing in a pool with cool, blue water. The person looks comfortable and refreshed, floating on their back with a serene expression. Wavy lines surround the person, indicating the coolness of the water. In the top right corner, there's a simple thermometer icon showing a low temperature. The overall color palette is dominated by refreshing blue tones. The image has a calm and soothing atmosphere.'''],

    ['''not found''',
     '''A person swimming backstroke in a clear blue swimming pool. The swimmer is on their back, arms raised above the water in mid-stroke, creating circular motions. The pool has lane markers visible. The swimmer's face is partially visible, looking up at the sky. There's splashing water around the swimmer's arms. At the bottom of the image, there's a semi-transparent text overlay that says "Backstroke" in large, white, sans-serif font.'''],
]

test_cases = {
    "默认": case_default[:10]
}

headers = ["序号", "指令", "prompt", "图片", "美学得分", "指令遵循得分"]


@dataclass
class Sample:
    index: int = 0
    instruction: str = "not found"
    prompt: str = ""
    image: str = None
    aesthetic_score: float = 0.
    clip_score: float = 0.

    def encode(self):
        return [self.index, self.instruction, self.prompt, self.image, self.aesthetic_score, self.clip_score]


class Evaluator:
    outputs = []
    samples = []
    eval_id = None
    evaluator = None
    pool = ThreadPoolExecutor(max_workers=1)

    @classmethod
    def preview(cls, case_name):
        if case_name is None:
            raise ValueError("请设置测试集")
        assert case_name in test_cases, f"没有找到测试集：{case_name}"
        cases = test_cases[case_name]

        samples = [Sample(index=i + 1, instruction=s[0], prompt=s[1]) for i, s in enumerate(cases)]
        return [s.encode() for s in samples]

    @classmethod
    def evaluate(cls, dataset_name, preset_name):
        if dataset_name is None:
            raise ValueError("请设置测试集")
        if preset_name is None:
            raise ValueError("请设置预设")
        assert dataset_name in test_cases, f"找不到测试集：{dataset_name}"
        assert preset_name in available_presets, f"找不到预设: {preset_name}"
        cls.eval_id = uuid.uuid4()

        cases = test_cases[dataset_name]
        samples = []

        for i, s in enumerate(cases):
            s = Sample(index=i + 1, instruction=s[0], prompt=s[1])

            preset = available_presets[preset_name]
            pipe = SDXLPipeline(preset)

            res, _ = pipe.run(payload=Payload(prompt=s.prompt), enable_preview=False)
            img = res[0]
            text = s.prompt[:75]  # todo : fix
            eval = cls.evaluator.evaluate_single(img, text)

            d = [
                ("preset", preset_name),
                ("test_dataset", dataset_name),
                ("index", s.index),
                ("instruction", s.instruction),
                ("prompt", s.prompt),
            ]
            s.image = Image.open(log_img(img, d)).convert("RGB")
            s.aesthetic_score = round(float(eval.aesthetic_score), 2)
            s.clip_score = round(float(eval.clip_score), 2)

            samples.append(s.encode())

            progress = int(100 * (i + 1) / len(cases))
            cls.outputs.append([progress, f"评估进度{i + 1}/{len(cases)}", None])
            cls.samples = copy.deepcopy(samples)

        return samples

    @classmethod
    def submit(cls, case_name, preset):
        cls.outputs.clear()
        cls.samples.clear()
        cls.eval_id = None
        # lazy load
        if cls.evaluator is None:
            cls.evaluator = ImageEvaluator()
        return cls.pool.submit(cls.evaluate, case_name, preset)

    @classmethod
    def report(cls):
        aesthetic_scores = []
        clip_scores = []

        for s in cls.samples:
            aesthetic_scores.append(s[-2])
            clip_scores.append(s[-1])

        s1_mean = np.mean(aesthetic_scores)
        s1_median = np.median(aesthetic_scores)
        s1_bad_cases = np.argsort(aesthetic_scores)[:5]
        s1_std = np.std(aesthetic_scores)

        s2_mean = np.mean(clip_scores)
        s2_median = np.median(clip_scores)
        s2_bad_cases = np.argsort(clip_scores)[:5]
        s2_std = np.std(clip_scores)

        d = [
            ("评估任务id", cls.eval_id),
            ("<美学评分>均值", f"{s1_mean:.2f}"),
            ("<美学评分>中位数", f"{s1_median:.2f}"),
            ("<美学评分>方差", f"{s1_std:.2f}"),
            ("<美学评分>分数最低（top5）", s1_bad_cases),

            ("<指令遵循评分>均值", f"{s2_mean:.2f}"),
            ("<指令遵循评分>中位数", f"{s2_median:.2f}"),
            ("<指令遵循评分>方差", f"{s2_std:.2f}"),
            ("<指令遵循评分>分数最低（top5）", s2_bad_cases),
        ]

        log_evaluation(d)
        return pretty_eval_report(d)
