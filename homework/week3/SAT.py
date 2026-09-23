from typing import List, Dict, Set

Clause = List[str]
CNF = List[Clause]


def extract_variables(cnf: CNF) -> List[str]:
    """提取公式中所有不重複的變數名"""
    variables: Set[str] = set()
    for clause in cnf:
        for lit in clause:
            variables.add(lit.lstrip("~"))
    return sorted(list(variables))


def evaluate_literal(lit: str, assignment: Dict[str, bool]) -> bool:
    """計算單一文字（Literal）的布爾值"""
    if lit.startswith("~"):
        return not assignment[lit[1:]]
    return assignment[lit]


def evaluate_clause(clause: Clause, assignment: Dict[str, bool]) -> bool:
    """計算單一子句（OR 運算）"""
    return any(evaluate_literal(lit, assignment) for lit in clause)


def solve_sat_by_truth_table_nobitertools(cnf: CNF):
    """
    不使用 itertools，利用二進位位元列舉 2^n 種真值表組合
    """
    vars_list = extract_variables(cnf)
    n = len(vars_list)
    total_combinations = 1 << n  # 等同於 2^n
    satisfying_assignments: List[Dict[str, bool]] = []

    # 表格標頭排版
    clause_headers = [" ∨ ".join(c) for c in cnf]
    var_header = " | ".join(f"{v:^5}" for v in vars_list)
    clause_header_str = " | ".join(f"{c:^12}" for c in clause_headers)
    divider = "-" * (len(var_header) + len(clause_header_str) + 25)

    print(f"\n[ 變數個數 ]: {n} (共 {total_combinations} 種賦值組合)")
    print(divider)
    print(f"{var_header} || {clause_header_str} || {'整體 (AND)':^10}")
    print(divider)

    # 核心：由 0 數到 (2^n - 1)
    for mask in range(total_combinations):
        assignment: Dict[str, bool] = {}
        for j, var in enumerate(vars_list):
            # 取出 mask 的第 (n - 1 - j) 位元（確保從 000, 001 到 111 順序遞增）
            bit = (mask >> (n - 1 - j)) & 1
            assignment[var] = bool(bit)

        # 計算各子句結果
        clause_results = [evaluate_clause(c, assignment) for c in cnf]
        cnf_result = all(clause_results)

        if cnf_result:
            satisfying_assignments.append(assignment)

        # 輸出單列結果
        var_vals = " | ".join(f"{('T' if assignment[v] else 'F'):^5}" for v in vars_list)
        clause_vals = " | ".join(f"{('T' if cr else 'F'):^12}" for cr in clause_results)
        final_str = f"{('★ SAT' if cnf_result else 'UNSAT'):^10}"

        print(f"{var_vals} || {clause_vals} || {final_str}")

    print(divider)

    # 輸出解
    if satisfying_assignments:
        print(f"\n結論: SATISFIABLE (可滿足)！找到 {len(satisfying_assignments)} 組解：")
        for i, sol in enumerate(satisfying_assignments, 1):
            sol_str = ", ".join(f"{k}={'T' if v else 'F'}" for k, v in sol.items())
            print(f"  解 {i}: ({sol_str})")
    else:
        print("\n結論: UNSATISFIABLE (不可滿足)，不存在任何賦值能使全式為真。")


# ===================== 測試 =====================
if __name__ == "__main__":
    # 公式：(A ∨ ~B) ∧ (~A ∨ C) ∧ (B ∨ ~C)
    cnf_test: CNF = [
        ["A", "~B"],
        ["~A", "C"],
        ["B", "~C"]
    ]
    solve_sat_by_truth_table_nobitertools(cnf_test)