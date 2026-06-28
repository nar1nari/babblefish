import argostranslate.package
import argostranslate.translate


def is_translation_installed(from_code: str, to_code: str) -> bool:
    if from_code == to_code or from_code == "auto":
        return True

    installed = argostranslate.translate.get_installed_languages()
    from_lang = next((l for l in installed if l.code == from_code), None)
    to_lang = next((l for l in installed if l.code == to_code), None)

    if from_lang and to_lang:
        if from_lang.get_translation(to_lang) is not None:
            return True
    return False


def install_translation(from_code: str, to_code: str):
    if from_code == to_code or from_code == "auto":
        return

    argostranslate.package.update_package_index()
    available = argostranslate.package.get_available_packages()

    direct = next(
        (p for p in available if p.from_code == from_code and p.to_code == to_code),
        None,
    )
    if direct:
        argostranslate.package.install_from_path(direct.download())
        return

    if from_code != "en" and to_code != "en":
        to_en = next(
            (p for p in available if p.from_code == from_code and p.to_code == "en"),
            None,
        )
        from_en = next(
            (p for p in available if p.from_code == "en" and p.to_code == to_code), None
        )

        if to_en and from_en:
            argostranslate.package.install_from_path(to_en.download())
            argostranslate.package.install_from_path(from_en.download())

    try:
        argostranslate.translate.clear_cache()
    except AttributeError:
        if hasattr(argostranslate.translate.get_installed_languages, "cache_clear"):
            argostranslate.translate.get_installed_languages.cache_clear()
        if hasattr(argostranslate.package.get_installed_packages, "cache_clear"):
            argostranslate.package.get_installed_packages.cache_clear()
