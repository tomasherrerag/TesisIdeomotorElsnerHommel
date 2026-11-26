import optuna


DB = "sqlite:///exp1Default.db"


def mostrar_trial(trial):

    print("=" * 70)
    print(f"TRIAL: {trial.number}")
    print("=" * 70)

    print("\nParámetros:")
    for nombre, valor in trial.params.items():
        print(f"  {nombre}: {valor}")

    print("\nUser attributes:")
    for nombre, valor in trial.user_attrs.items():
        print(f"  {nombre}: {valor}")


if __name__ == "__main__":

    study = optuna.load_study(
        study_name="exp1Default",
        storage=DB
    )

    print("=" * 70)
    print("SCANNER EXPERIMENTACIÓN EXP1")
    print("=" * 70)

    print(f"\nNúmero de trials: {len(study.trials)}")

    # Mostrar algunos trials para comprobar
    # cómo fueron almacenados los datos.
    cantidad = min(3, len(study.trials))

    for trial in study.trials[:cantidad]:
        mostrar_trial(trial)
        print()