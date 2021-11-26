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
#version 460
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoords;
layout(location = 2) in vec3 normal;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform vec3 pointLight;
out float intensity;
out vec2 outTextCoords;

void main()
{

  vec4 normVec = vec4(normal, 0.0);
  vec4 posVec = vec4(position, 1.0);
  posVec = modelMatrix * posVec;
  vec4 light = vec4(pointLight, 1.0);
  intensity = dot(modelMatrix * normVec, normalize(light - posVec));
  gl_Position = projectionMatrix * viewMatrix * modelMatrix * posVec;
  outTextCoords = texCoords;
}
"""


toon_shader_fragment = """
#version 460
layout(location = 0) out vec4 fragColor;
in float intensity;
in vec2 outTextCoords;
uniform sampler2D textCoords;

void main()
{

  if (intensity > 0.75) {
    fragColor = vec4(1.0, 1.0, 1.0, 1.0) * texture(textCoords, outTextCoords);
  } 
  else if (intensity > 0.50) {
    fragColor = vec4(0.65, 0.65, 0.65, 1.0) * texture(textCoords, outTextCoords);
  } 
  else if (intensity > 0.25) {
    fragColor = vec4(0.45, 0.45, 0.45, 1.0) * texture(textCoords, outTextCoords);
  } 
  else {
    fragColor = vec4(0.3, 0.3, 0.3, 1.0) * texture(textCoords, outTextCoords);
  }
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

