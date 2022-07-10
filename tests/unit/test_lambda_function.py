from src.lambda_function import LambdaHandler, LambdaEnviron


def test_lambda_handler_ok():
    # 初期化
    lambda_env = LambdaEnviron("test")

    class MockDb():
        def get_item(self, table_name: str, pkey: str):
            return {"table_name": table_name, "pkey": pkey}

    handler = LambdaHandler(lambda_env, MockDb(), "sample")

    # テスト実施
    result = handler()

    # 期待値比較
    code = result["code"]
    assert code == 200
    item = result["item"]
    assert item == {"table_name": "test", "pkey": "sample"}
