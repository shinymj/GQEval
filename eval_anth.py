import json
import anthropic
import os
import datetime
import re

# Set Anthropic
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL_NAME = 'claude-3-5-sonnet-20240620'
MODEL_TEMPERATURE = 0
MAX_TOKENS = 1500


# Set rubric variable
RUBRIC_VARIABLES = {
    "answerer": "user who requested",
    "goal": "resolving uncertainty by acquiring useful information"
}

## answerer
# scene member, user who requested, average person
## goal
# icebreaking for social interaction, resolving uncertainty by acquiring useful information

input_path = "FILENAME.json" # put the file in _src/ folder 
rubric_path = "Rubric_GQ.json"
system_prompt_file = "system_prompt.txt"

def read_file(file_path, is_json=False):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file) if is_json else file.read()

def apply_variables_to_rubric(rubric, variables):
    """루브릭의 텍스트에 변수를 적용합니다."""
    rubric_str = json.dumps(rubric, ensure_ascii=False)
    
    # ${변수명}과 &{변수명} 두 가지 형식 모두 처리
    for var_name, var_value in variables.items():
        rubric_str = rubric_str.replace(f"${{{var_name}}}", var_value)
        rubric_str = rubric_str.replace(f"&{{{var_name}}}", var_value)
    
    return json.loads(rubric_str)

def evaluate_fq(context, fq, rubric, system_prompt_content):
    
    # 변수가 적용된 루브릭 생성
    processed_rubric = apply_variables_to_rubric(rubric, RUBRIC_VARIABLES)

    system_prompt = system_prompt_content.format(
        rubric=json.dumps(processed_rubric, ensure_ascii=False, indent=2),
        context=json.dumps(context, ensure_ascii=False),
        fq=fq
    )
    user_message = "Please rate each criterion on a scale of 1-5 and provide a rationale in Korean for each score."

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        temperature=MODEL_TEMPERATURE,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    
    # JSON 부분만 추출
    content = response.content[0].text
    json_matches = re.findall(r'\[.*?\]', content, re.DOTALL)
    
    if json_matches:
        try:
            return json.loads(json_matches[-1])  # 마지막으로 매치된 JSON 사용
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {e}")
            print(f"파싱 시도한 문자열: {json_matches[-1]}")
    else:
        print("JSON 형식의 응답을 찾을 수 없습니다.")

    return []

def main():
    sample = read_file(f'_src/{input_path}', is_json=True)
    rubric = read_file(rubric_path, is_json=True)
    system_prompt_content = read_file(system_prompt_file)

    # 디버깅을 위해 변수 적용된 루브릭 출력
    processed_rubric = apply_variables_to_rubric(rubric, RUBRIC_VARIABLES)
    print("변수 적용된 루브릭:")
    print(json.dumps(processed_rubric, ensure_ascii=False, indent=2))

    results = []
    for item in sample:
        evaluation = evaluate_fq(item['context'], item['follow-up']['FQ'], rubric, system_prompt_content)
        results.append({
            "context": item['context'],
            "follow-up": item['follow-up'],
            "evaluation": evaluation
        })
        print(f"Processed item. Evaluation result: {evaluation}")  # 디버깅용 출력

    # 최종 출력 데이터 구조화
    output_data = {
        "metadata" : [{"model":MODEL_NAME, "temperature":MODEL_TEMPERATURE}],
        "processed_rubric": processed_rubric,
        "results": results
    }

    now = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    with open(f'_output/{now}_anth_{input_path}', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()