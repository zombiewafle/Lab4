# GLSL

vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float tiempo;
uniform float valor;
uniform vec3 pointLight;

out vec3 outColor;
out vec2 outTexCoords;

void main()
{
    vec4 norm = vec4(normal, 0.0);

    vec4 pos = vec4(position, 1.0) + norm * valor;
    pos = modelMatrix * pos;

    vec4 light = vec4(pointLight, 1.0);

    float intensity = dot(modelMatrix * norm, normalize(light - pos));

    gl_Position = projectionMatrix * viewMatrix * pos;

    outColor = vec3(1.0,1.0 - valor * 2,1.0-valor * 2) * intensity;
    outTexCoords = texCoords;
}
"""

toon_shader_Vertex = """
#version 330 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 uv;
 
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform mat4 mvpMatrix;
uniform vec3 eyePos;
uniform float time;
 
out vec3 fsNormal;
out vec2 fsUV;
 
void main()
{
    vec4 pos = mvpMatrix * vec4(position.xyz, 1);
    fsNormal = vec3(modelMatrix * viewMatrix * vec4(normal, 0)).xyz;
    fsUV = uv;
    gl_Position = pos;
}
"""

toon_shader_fragment = """
	
#version 330 core
out vec4 FragColor;
 
in vec3 fsNormal;
in vec2 fsUV;
 
uniform vec3 eyePos;
uniform sampler2D mainTexture;
uniform sampler2D rampTexture;
 
void main()
{
    vec3 lightDir = normalize(vec3(0, 0, 1));
 
    vec3 normal = normalize(fsNormal);
 
    float nDotl = clamp(dot(normal, lightDir), 0, 1);
 
    float ramp = texture(rampTexture, vec2(nDotl, 0.5)).r;
 
    vec3 albedo = texture(mainTexture, fsUV).rgb;
    vec3 diffuse = albedo * pow(ramp, 1.3);
    FragColor = vec4(diffuse, 1.0f);
}
"""


fragment_shader = """
#version 460
layout (location = 0) out vec4 fragColor;

in vec3 outColor;
in vec2 outTexCoords;

uniform sampler2D tex;

void main()
{
    fragColor = vec4(outColor, 1) * texture(tex, outTexCoords);
}
"""

