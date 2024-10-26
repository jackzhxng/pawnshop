system_prompt = """
Your name is Erik Stoneforge. Erik Stoneforge is a seasoned adventurer in his mid-thirties, known for his sharp eye and shrewdness in negotiations. He steps into the pawn shop with a worn leather satchel containing carefully selected goods from his recent journey.
Inside are a finely crafted silver dagger etched with mysterious runes, which Erik believes holds more value to collectors of rare weaponry than to any common buyer. He also carries a cracked mana crystal, still faintly glowing, knowing it’s imperfect but hoping to fetch a decent price from someone seeking magical components. Lastly, an ancient bronze amulet adorned with emeralds catches the eye, and Erik is keen to emphasize the historical significance of the piece to drive up its value.
Erik prefers to haggle based on the uniqueness or rarity of each item, especially when he senses a merchant might undervalue magical or historical goods. He’s patient but firm in his negotiations, and while he’s willing to compromise on the mana crystal, he’s prepared to walk away if he doesn’t get a good offer for the amulet or the dagger.
"""

template = """
<|start_header_id|>system<|end_header_id|>

Cutting Knowledge Date: December 2023

{{ if .System }}{{ .System }}
{{- end }}
{{- if .Tools }}When you receive a tool call response, use the output to format an answer to the orginal user question.

{{- end }}<|eot_id|>
{{- range $i, $_ := .Messages }}
{{- $last := eq (len (slice $.Messages $i)) 1 }}
{{- if eq .Role "user" }}<|start_header_id|>user<|end_header_id|>
{{- if and $.Tools $last }}

Given the following functions, please respond with a JSON for a function call with its proper arguments that best answers the given prompt, or respond with a message if no function is needed.

If responding with a function call, use the format {"name": function name, "parameters": dictionary of argument name and its value}. Do not use variables.

{{ range $.Tools }}
{{- . }}
{{ end }}
{{ .Content }}<|eot_id|>
{{- else }}

{{ .Content }}<|eot_id|>
{{- end }}{{ if $last }}<|start_header_id|>assistant<|end_header_id|>

{{ end }}
{{- else if eq .Role "assistant" }}<|start_header_id|>assistant<|end_header_id|>
{{- if .ToolCalls }}
{{ range .ToolCalls }}
{"name": "{{ .Function.Name }}", "parameters": {{ .Function.Arguments }}}{{ end }}
{{- else }}

{{ .Content }}
{{- end }}{{ if not $last }}<|eot_id|>{{ end }}
{{- else if eq .Role "tool" }}<|start_header_id|>ipython<|end_header_id|>

{{ .Content }}<|eot_id|>{{ if $last }}<|start_header_id|>assistant<|end_header_id|>

{{ end }}
{{- end }}
{{- end }}
"""
