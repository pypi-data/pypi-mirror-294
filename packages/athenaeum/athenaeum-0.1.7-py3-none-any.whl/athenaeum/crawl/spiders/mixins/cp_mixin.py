import time
import atexit
from DrissionPage import ChromiumPage, ChromiumOptions
from typing import Optional
from athenaeum.chrome_extension import ChromeExtension

CO_TYPE = ChromiumOptions
TIMEOUT_TYPE = float
IS_CLOSE_TYPE = bool
CP_TYPE = ChromiumPage


class CpMixin(object):

    def __init__(self, *,
                 co: Optional[CO_TYPE] = None,
                 timeout: Optional[TIMEOUT_TYPE] = None,
                 is_close_cp: Optional[IS_CLOSE_TYPE] = None,
                 cp: Optional[CP_TYPE] = None,
                 **co_kwargs):
        self.co = co
        self.timeout = timeout
        self.is_close_cp = is_close_cp
        self.cp = cp
        self.co_kwargs = co_kwargs

        self._init()

    def _init(self):
        self._init_co()

        if self.timeout is None:
            self.timeout = 10.0

        if self.is_close_cp is None:
            self.is_close_cp = False

        self._init_cp()

        atexit.register(self.close_cp)

    def _init_co(self) -> None:
        if self.co is not None:
            return
        self.co = self.create_co()

    def create_co(self, **kwargs) -> CO_TYPE:
        co = ChromiumOptions()

        if not kwargs:
            kwargs = self.co_kwargs

        port = kwargs.get('port')
        auto_port = kwargs.get('auto_port', True)
        add_extension = kwargs.get('add_extension', False)
        use_system_user_path = kwargs.get('use_system_user_path', False)
        headless = kwargs.get('headless', False)
        mute = kwargs.get('mute', True)
        incognito = kwargs.get('incognito', False)
        ignore_certificate_errors = kwargs.get('ignore_certificate_errors', False)

        if add_extension:
            ce = ChromeExtension()
            for extension_path in ce.extension_paths:
                co.add_extension(extension_path)

        if port is not None:
            co.set_local_port(port=port)  # 此方法用于设置本地启动端口
        else:
            co.auto_port(on_off=auto_port)
        co.use_system_user_path(on_off=use_system_user_path)  # 此方法设置是否使用系统安装的浏览器默认用户文件夹
        co.headless(on_off=headless)
        co.mute(on_off=mute)
        co.incognito(on_off=incognito)  # 该方法用于设置是否以无痕模式启动浏览器
        co.ignore_certificate_errors(on_off=ignore_certificate_errors)

        # 阻止 “自动保存密码” 的提示气泡
        co.set_pref('credentials_enable_service', False)
        # 阻止 “要恢复页面吗？Chrome未正确关闭” 的提示气泡
        co.set_argument('--hide-crash-restore-bubble')

        return co

    def _init_cp(self) -> None:
        if self.cp is not None:
            return
        self.cp = self.create_cp(self.co)
        self.is_close_cp = True

    def create_cp(self, addr_or_opts, tab_id=None, timeout: Optional[TIMEOUT_TYPE] = None) -> CP_TYPE:
        if timeout is None:
            timeout = self.timeout
        ChromiumPage._PAGES = {}
        cp = ChromiumPage(addr_or_opts, tab_id, timeout)
        cp.set.window.mini()
        return cp

    def close_cp(self) -> None:
        if self.is_close_cp and self.cp is not None and self.cp.process_id and self.cp.tab_id:
            self.cp.close()
            self.cp = None

    def wait_complete(self, cp: Optional[CP_TYPE] = None) -> None:
        if cp is None:
            cp = self.cp
        while True:
            if cp.states.ready_state == 'complete':
                break

    def wait_document_reload(self, cp: Optional[CP_TYPE] = None) -> None:
        """
        等待页面重新载入
        :param cp:
        :return:
        """
        if cp is None:
            cp = self.cp
        while True:
            if cp.wait.load_start() is False and cp.wait.doc_loaded() is True:
                break

    def wait_fetch_or_xhr_reload(self, loc_or_ele: str, timeout: Optional[TIMEOUT_TYPE] = None,
                                 cp: Optional[CP_TYPE] = None) -> None:
        """
        等待 loading 的元素消失
        :param loc_or_ele:
        :param timeout:
        :param cp:
        :return:
        """
        if timeout is None:
            timeout = self.timeout
        if cp is None:
            cp = self.cp

        start_time = time.time()
        while True:
            end_time = time.time()
            if end_time - start_time > timeout:
                break
            if cp.wait.ele_displayed(loc_or_ele) is False or cp.wait.ele_deleted(loc_or_ele) is True:
                break

    def refresh(self, cp: Optional[CP_TYPE] = None,
                *refresh_args, **refresh_kwargs) -> None:
        if cp is None:
            cp = self.cp
        js_code = '''function hasOverflowElement(){const elements=document.querySelectorAll('*:not(script):not(style)');for(let element of elements){if(element.offsetWidth>window.innerWidth){return true}}return false};hasOverflowElement();'''
        ret = cp.run_js(js_code)
        if not ret:
            cp.refresh(*refresh_args, **refresh_kwargs)
            return

        tb = cp.new_tab(cp.url)
        self.close_cp()
        cp = self.create_cp(tb.address, tb.tab_id)
        self.cp = cp
if __name__ == '__main__':
    CpMixin()