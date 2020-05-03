---
layout: post
title: "Creativity through limitation: Shadertoy"
description: "Shadertoy is a place where anyone can share realtime procedural graphics experiments. This article is an introduction to procedural graphics and ray tracing."
image: /assets/blog-images/2019-08-17-cover.jpg
tags: [programming]
---

This is the third article in “Creativity through limitation” series. In case you missed the previous ones:

- [8-bit demoscene]({% link _posts/2018-08-05-creativity-through-limitation-8-bit-demoscene.md %})
- [PICO-8 — Fantasy console]({% link _posts/2019-06-18-creativity-through-limitation-pico-8.md %})

When I first learned about [Shadertoy](https://www.shadertoy.com) and browsed through some works there, my reaction was: “HOW???!!!” I already knew what shaders are because I’m interested in computer graphics and learned OpenGL basics. This knowledge only amplified my fascination.

Shadertoy is a place where anyone can share their experiments with realtime procedural computer graphics. It is created by [Inigo Quilez](http://iquilezles.org/index.html) (a demoscener and a former Pixar employee) and [Pol Jeremias](http://www.poljeremias.com) (currently working at Pixar). It uses WebGL, so everything runs right in a browser.

Here’s an example of what people do:

<iframe width="640" height="360" frameborder="0" src="https://www.shadertoy.com/embed/XsBXWt?gui=true&t=10&paused=true&muted=false" allowfullscreen></iframe>

<p class="footnote">Click the “play” button to see it in action.</p>

You may think that it looks pretty simple compared to, for example, the latest video games. Let me give you a quick high-level introduction to 3D graphics (CG-pros, if you read it, don’t blame me for the oversimplification, please). To draw some 3D object, you need to model it with triangles, define transformations (rotation, scaling, projection, etc.) and then use some shader magic. Shaders are small programs running on GPU — graphics processing unit on a video card. First, you pass all polygon vertices and transformations to vertex shaders. They convert 3D coordinates to 2D screen coordinates and pass all data to a rasterizer. Rasterizer draws triangles and calls fragment shaders for each pixel to get the color.

Sounds simple? Then remove everything but a fragment shader. The only input you have now is a coordinate on a screen. Try to think about how to draw a 3D cube. Shaders run in parallel on multiple GPU cores, so you can’t have any state to pass between shader calls while drawing a single frame. Shaders are just like functions in functional programming languages, or mathematical functions — they can’t have side effects. Does it sound challenging and limiting now? I believe that your answer is “YES!”

## How to draw a disk with a fragment shader

Shaders are written in GLSL language; the syntax is very similar to C. GLSL has a lot of built-in data types and functions to work with vectors and matrices. Writing your first fragment shader is a mind-shifting experience. Even drawing a disk (a filled circle) is a tricky task in the beginning. Let’s do it now.

As you remember, the only input we have in a fragment shader is a screen coordinate. To draw a disk we need to check if this pixel is inside it or not. Let’s remember the definitions:

> A disk is the region in a plane bounded by a circle.
>
> A circle is the set of all points in a plane that are at a given distance (the radius) from a given point (the center).

So, if the distance from the center is less than the radius, then the point is inside the disk, otherwise — it’s outside. To calculate the distance from an origin point, we use the following formula: sqrt(x² + y²). Given that, to draw a disk, we need to check each pixel for sqrt(x² + y²) \< r, or x² + y² \< r² (it’s the disk formula in Cartesian coordinates). Now let’s look at the shader code:

```glsl
void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    // Normalize coordinates to (-1, 1) range and correct aspect ratio
    vec2 uv = fragCoord.xy / iResolution.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= iResolution.x / iResolution.y;

    // Check if the point is inside the circle
    if (uv.x * uv.x + uv.y * uv.y < 0.3) {
        fragColor = vec4(1, 1, 1, 1);
    } else {
        fragColor = vec4(0, 0, 0, 1);
    }
}
```

`fragCoord` is the input variable with screen coordinates. For the ease of use, we convert it to a (-1, 1) range. `fragColor` is the output variable for a pixel color. `iResolution` is a uniform variable — a global value that doesn’t change while drawing a frame. Shadertoy provides some other convenient uniform variables, for example, `iTime` — a time passed since shader start in seconds, which you can use for animations.

<iframe frameborder="0" src="https://www.shadertoy.com/embed/wtSXWD?gui=true&t=10&paused=true&muted=false" allowfullscreen></iframe>

## Ray tracing with fragment shaders

Now let’s do something more complicated — ray tracing.

> Ray tracing is a rendering technique for generating an image by tracing the path of light as pixels in an image plane and simulating the effects of its encounters with virtual objects — [Wikipedia](https://en.wikipedia.org/wiki/Ray_tracing_(graphics))

I think ray tracing is the best way to draw 3D scenes with fragment shaders because they naturally match the idea of ray tracing. If you read the code of some shaders at Shadertoy, you’ll see that most of them use it in some form.

I wrote my first ray tracing shader for this article, here’s my final result:

<iframe frameborder="0" src="https://www.shadertoy.com/embed/tlXXzB?gui=true&t=10&paused=true&muted=false" allowfullscreen></iframe>

My shader doesn’t work in Safari because it doesn’t support WebGL 2 yet. You can enable experimental support from the development menu (Develop → Experimental Features → WebGL 2.0). I’d recommend using Google Chrome with Shadertoy.

You can see the full code at Shadertoy. It’s a fantastic feature of Shadertoy which I love — all code is open, and you can learn from it. I added quite a lot of comments to make it easy to understand for beginners. Here I want to walk through the code and give a bit more details.

`mainImage` function is pretty straightforward: I normalize screen coordinates, just like in the disk example above, then I set camera position and the ray direction — `camO` and `camL` variables. All ray tracing code is in the separate function to improve the structure and readability.

```glsl
void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = fragCoord.xy / iResolution.xy;
    uv = uv * 2.0 - 1.0;
    uv.x *= iResolution.x / iResolution.y;

    // Camera
    vec3 camO = vec3(0, 0, 0);
    vec3 camL = normalize(vec3(uv.x, uv.y, 7));

    // Ray-tracing
    fragColor = vec4(trace(camO, camL), 1.);
}
```

In the beginning, I define my scene: a light source, three spheres, and a “floor,” which is yet another sphere, but very big, so it looks almost flat. By the way, this code is why the shader doesn’t work in Safari by default — there’s no array support in WebGL 1.

`COUNT` is the number of objects, `SIZE` is the number of array items for each object. For each sphere, I define the starting position and the radius, color, movement speed, and movement amplitude for each axis. Using arrays in this example is more convenient than adding multiple conditions in the code.

```glsl
#define COUNT 5
#define SIZE 4

vec4 spheres[] = vec4[COUNT * SIZE](
    // Spheres: center and radius, color, movement speed, movement amplitude
    // Light source
    vec4(-7.5, 0., 31., 0.1), vec4(1., 1., 1., 1.),
    vec4(2., 1., 0, 0), vec4(0, 2., 0, 0),
    // 1
    vec4(-4., 0., 39., 2), vec4(.2, .9, .2, 1.),
    vec4(1., 1.1, 2., 0), vec4(2, 3, 5.1, 0),
    // 2
    vec4(3., 0., 42., 3.), vec4(.9, .4, .5, 1.),
    vec4(1.3, 1.7, 1.5, 0), vec4(1, 4, 5.1, 0),
    // 3
    vec4(2, -1., 43., 1.5), vec4(.2, .3, 1., 1.),
    vec4(2., 1., 2., 0), vec4(7, 1, 7, 0),
    // "Floor"
    vec4(0, -800006, 0, 800000), vec4(1.7, 1.0, .7, 1),
    vec4(0, 0, 0, 0), vec4(0, 0, 0, 0)
);
```

I want my spheres to move, so the next helper function calculates the position of each sphere at any moment. I moved this code to a separate function because I use it in multiple places. I use `iTime` uniform variable to do the animation. I used `cos` instead of `sin` for Z-axis to do circular flying trajectory for a blue ball. I could add another object parameter in the array above for the phase shift for each axis but decided to keep it simple.

```glsl
vec3 sphereCenter(int sphere) {
    vec4 sD = spheres[sphere * SIZE];
    vec4 sS = spheres[sphere * SIZE + 2];
    vec4 sA = spheres[sphere * SIZE + 3];
    vec3 c = vec3(
        sD.x + sin(iTime * sS.x) * sA.x,
        sD.y + sin(iTime * sS.y) * sA.y,
        sD.z + cos(iTime * sS.z) * sA.z);
    return c;
}
```

`findIntersection` is a crucial function. It finds the intersection between a ray and a sphere and returns sphere number and distance between the ray origin point (`o`) and the intersection point. The ray can intersect multiple spheres in multiple points, but we need only the nearest intersection point. I took the formula for a line-sphere intersection from [this Wikipedia article](https://en.wikipedia.org/wiki/Line%E2%80%93sphere_intersection), so I won’t dig into the details here. `ignore` variable allows me to ignore a single sphere from checking intersections, I use it for shadows.

```glsl
int findIntersection(vec3 o, vec3 l, int ignore, out float d) {
    int sphere = -1;
    d = 1e5;

    for (int i = 0; i < COUNT; i++) {
        if (i == ignore) {
            continue;
        }
        vec3 c = sphereCenter(i);
        float r = spheres[i * SIZE].w;

        // Ray-sphere intersection formula
        vec3 t1 = o - c;
        float t1l = length(t1);
        float t2 = dot(l, t1);
        float s = t2 * t2 - t1l * t1l + r * r;
        if (s >= 0.) {
            float ss = sqrt(s);
            float sd = min(-t2 + ss, -t2 - ss);
            if (sd >= 0. && sd < d) {
                sphere = i;
                d = sd;
            }
        }
    }
    return sphere;
}
```

`trace` function connects all the pieces. It traces a single ray (`camO` is the origin, `camL` is the direction) for a screen pixel and returns a color value for this pixel. We check if there’s any sphere in this direction; if the answer is “yes” — apply lighting to it, otherwise return background color.

The light source is also a sphere, but we don’t need to apply any lighting to it, that’s why there’s a particular check for it.

I combine three lighting elements here (you can see them summed in the final `return` statement):

- ambient lighting (`aColor` variable)
- diffusion lighting
- specular lighting

I took all formulas from [“Basic shading” OpenGL tutorial](http://www.opengl-tutorial.org/beginners-tutorials/tutorial-8-basic-shading/), it has clear and easy to understand explanations, so, again, I’m not digging into details here. The only thing I added myself was shadowing — I wanted spheres to cast shadows on other objects. It was easy to do: I trace another ray from an intersection point to the light source, and if there’s something between, then this object is under the shadow.

```glsl
#define LIGHT_POWER 80.
#define SPECULAR_POWER 20.
#define AMBIENT .3

vec3 trace(vec3 camO, vec3 camL) {
    float d = 0.;
    int sphere = findIntersection(camO, camL, -1, d);

    if (sphere == -1) {
        // There was no intersection, return background color
        return vec3(0, 0, 0);
    }

    vec3 lightColor = spheres[1].xyz;

    if (sphere == 0) {
        // It's a light source, don't need to shade it
        return lightColor;
    }

    vec3 lightPoint = sphereCenter(0);

    // Sphere color
    vec3 sColor = spheres[sphere * SIZE + 1].xyz;
    vec3 aColor = sColor * vec3(AMBIENT, AMBIENT, AMBIENT);

    // Intersection point
    vec3 iPoint = camO + camL * d;
    vec3 iNormal = normalize(iPoint - sphereCenter(sphere));

    // Light direction vector
    vec3 lightDir = normalize(lightPoint - iPoint);

    // Check if there's another sphere between this one and the light source
    float dShadow = 0.;
    int shadowedBy = findIntersection(iPoint, lightDir, sphere, dShadow);
    dShadow = float(shadowedBy + 1) / 5.0;
    if (shadowedBy != 0) {
        // We're under shadow, use ambient color
        return aColor;
    }

    // Lighting (diffusion and specular)
    float cosA = clamp(dot(iNormal, lightDir), 0., 1.);
    float cosS = clamp(dot(-camL, reflect(-lightDir, iNormal)), 0., 1.);

    float dSquared = pow(length(iPoint - lightPoint), 2.);

    return aColor +
        sColor * lightColor * cosA * LIGHT_POWER / dSquared +
        lightColor * pow(cosS, SPECULAR_POWER) * LIGHT_POWER / dSquared;
}
```

----

All the math above looked a bit complex to me at first, but when I did everything myself and fixed all the bugs (oh, I had plenty of them!), I grasped it. The next step would be to implement more complex models. One of the main challenges in ray tracing is finding the intersection point. It’s easy for a sphere, but it becomes difficult for other geometrical objects. The good news is that there’s a ray tracing technique called “ray marching” which makes finding intersection point simple even for very complex objects. Initially, I wanted to cover ray marching here, but if I’d done so, the article would have been much longer. If you’re interested in this topic, you may find these links useful:

- [“Ray marching and signed distance functions” by Jamie Wong](http://jamie-wong.com/2016/07/15/ray-marching-signed-distance-functions/) — it was an eye-opener for me, after reading it I understood how many Shadertoy masterpieces work.
- [“Primitives” by Inigo Quilez](http://iquilezles.org/www/articles/distfunctions/distfunctions.htm) — a reference to signed distance functions.

Shadertoy is a fantastic place, and I barely scratched the surface of its features. There’s much more: textures, handling user input, multiple buffers, “sound shaders,” etc. Just go to Shadertoy and explore it! I believe that you’ll find many mind-blowing shaders.
