/*
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
*/




/**Build a sub section of the original python file.
 * */
const toSection = (py_section, content) =>{
  return content && `\n\n# --- PYODIDE:${ py_section } --- #\n${ content }`
}





class IdeTesterGuiManager extends IdeRunner {

  constructor(editorId){
    super(editorId)
    this.delay       = 0     // Override: no pause when starting the executions
    this.conf        = null
    this.testing     = false
    this.toSwap      = [this.data, this.getCodeToTest] // nothing to swap...
    this.ides_cache  = {}
    this.test_cases  = []   // Linearized version of CASES_DATA
    this.std_capture = []   // Full stdout+stdErr capture, BEFORE any jQuery.terminal formatting
    this.counters    = {skip:0, remaining:0, failed:0, success:0}
  }

  // _init(){
  //   super._init()
  // }

  save(_){}

  isTesting(){
    return this.running == CONFIG.running.testing
  }


  // Override
  build(){
    super.build()
    const tester = this

    // configure "run all" button:
    $(this.globalIdH).parent()
                     .find('button[btn_kind=test_ides]')
                     .on('click', ()=>this.runAllTests())


    // Configure '"un-/select all" buttons:
    ;[ [false, ''], [true, 'un'] ].forEach(([state,prefix])=>{

      $(`button#${ prefix }select-all`).on('click', function(){
        tester.test_cases.forEach(o=>{
          o.skip = state
          tester.setSvgAndCounters(o, prefix+'checked')
        })
        tester.displayCounters()
      })
    })


    const handleConfSvgAndRuntime = (conf, individuals, tailId="") =>{
      this.test_cases.push(conf)
      individuals.push(conf)

      const svgId = `#${ conf.editor_id }-status${ tailId }`
      conf.divSvgBtnsId = svgId
      conf.fail = Boolean( conf.fail || conf.in_error_msg || conf.not_in_error_msg )
      if(conf.std_capture_regex){
        conf.std_capture_regex = new RegExp(conf.std_capture_regex)
      }

      if(conf.skip) this.counters.skip++
      else          this.counters.remaining++

      $(svgId)
          .html(CONFIG.QCM_SVG)
          .addClass([ 'multi', conf.skip ? 'unchecked':'checked' ])
          .on( 'click', function(){
              if(tester.testing) return;
              tester.setSvgAndCounters(conf, conf.skip ? 'checked':'unchecked')
              tester.displayCounters()
          })
    }

    const propsToReport = 'editor_id ide_link ide_name page_url rel_dir_url'.split(' ')
    const confs = Object.values(CASES_DATA)

    confs.forEach( conf =>{

      // Show what section will be tested (in the main test, at least):
      $(`#${ conf.editor_id }_${ conf.code ? 'code':'corr' }`).addClass('orange-box')

      const individuals = []
      if(!conf.then){
        handleConfSvgAndRuntime(conf, individuals)

      }else{
        conf.then.forEach( (subConf, i)=>{
          if(i) subConf.no_clear = true            // Keep original choice for first only
          for(const prop of propsToReport){
            subConf[prop] = conf[prop]
          }
          handleConfSvgAndRuntime(subConf, individuals, i+1)
        })
      }


      $(`#${ conf.editor_id }-test-btns > button[btn_kind=test_1_ide]`).on(
        'click', ()=>this.runAllTests(individuals)
      )
      $(`#${ conf.editor_id }-test-btns > button[btn_kind=load_ide]`).on(
        'click', this.loadFactory(conf)
      )
    })


    // Display initial counters state
    const nIdes   = confs.length
    const nTests  = this.test_cases.length
    const allHtml = nTests==nIdes ? nIdes : `${ nIdes }<br>(${ nTests } cases)`
    $('#cnt-all').html(allHtml)
    this.displayCounters()
  }


  /**Update the html class of the svg container with the given id.
   * */
  setSvgAndCounters(conf, kls){
    const div = $(conf.divSvgBtnsId)
    this.updateCountersFor(div, -1)
    div.removeClass(['checked', 'unchecked', 'correct', 'incorrect', 'must-fail'])
    div.addClass(kls)
    this.updateCountersFor(div, +1)
    conf.skip = div.hasClass('unchecked')
  }


  updateCountersFor(div, delta){
    if(div.hasClass('correct'))   this.counters.success   += delta
    if(div.hasClass('incorrect')) this.counters.failed    += delta
    if(div.hasClass('checked'))   this.counters.remaining += delta
    if(div.hasClass('unchecked')) this.counters.skipped   += delta
  }


  /**Update the values of each counter.
   * */
  displayCounters(){
    Object.entries(this.counters).forEach( ([cnt,n])=>{ $('#cnt-'+cnt).text(n) })
  }


  // Override
  terminalEcho(content){
    this.std_capture.push(content)
    super.terminalEcho(content)
  }


  swap(){
    ;[this.data, this.toSwap[0]]          = [this.toSwap[0], this.data]
    ;[this.getCodeToTest, this.toSwap[1]] = [this.toSwap[1], this.getCodeToTest]
  }


  // Override
  terminalDisplayOnStart(){
    if(this.isTesting()){
      this.terminal.clear()
      this.terminal.echo(`Testing: ${ this.conf.ide_name }`)
    }else{
      super.terminalDisplayOnStart()
    }
  }


  /**Extract the config object for the given IDE, getting rid of the profile data on the way.
   * Data are cached so that a page is requested once only.
   * */
  async getIdeData(conf){

    // Request + store the data for all the IDEs in the related page, if missing:
    if(!this.ides_cache[conf.editor_id]){

      const response = await fetch(conf.page_url)
      const html     = await response.text()

      const reg      = /(?<=PAGE_IDES_CONFIG\s*=\s*['"]).+?(?=["']\s*<\/script>)/
      const compress = html.match(reg)[0]                 // Does always match!
      const fix_comp = compress.replace(/\\x1e/g, "\x1e")
      const configs  = decompressAndConvert(fix_comp)

      Object.entries(configs).forEach( ([editor,data])=>{
        this.ides_cache[editor] = this._prepareData(data)
        conf.attempts_left = data.attempts_left
        conf.profile = data.profile
        if(!conf.keep_profile) data.profile = null   // Remove profile info for tests.
      })
    }
    return this.ides_cache[conf.editor_id]
  }





  /**Runtime to apply when clicking on a button to "download" all the code of an
   * IDE in the testing one.
   * */
  loadFactory(conf){
    return async ()=>{
      await waitForPyodideReady()

      if(this.testing) return;    // Deactivated during tests (otherwise, big troubles...)

      this.data = await this.getIdeData(conf)   // Update first (see getters)

      const sections = [
        toSection('env',       this.envContent),
        toSection('env_term',  this.envTermContent),
        toSection('corr',      this.corrContent),
        toSection('code',      this.userContent),
        toSection('post_term', this.postTermContent),
        toSection('post',      this.postContent),
      ]
      const codeToTest = sections.splice( 2+conf.code, 1)[0]
      const fullCode = [
        codeToTest,
        CONFIG.lang.tests.msg.trimEnd(),
        toSection('tests', this.publicTests),
        toSection('secrets', this.secretTests),
        `\n\n"""\n${ sections.join('').replace(/"""/g, '\\"\\"\\"').trimStart() }\n"""`
      ].join('')

      this.applyCodeToEditorAndSave(fullCode)
    }
  }
}














class IdeTester extends IdeTesterGuiManager {


  // Override
  handleRunOutcome(runtime, decrease_count){}


  // Override + global std observer
  // giveFeedback(stdout, stdErr="", _){
  //   this.std_capture.push(stdout+stdErr)
  //   super.giveFeedback(stdout, stdErr, _)
  // }



  async runAllTests(targets){
    await waitForPyodideReady()

    this.terminal.clear()
    const start = Date.now()
    this.testing = true

    const confsToRun = (targets ?? this.test_cases).filter( conf =>{
      const skip = (!targets || targets.length!=1) && conf.skip
      if(!skip){
        this.setSvgAndCounters(conf, 'checked')
      }
      return !skip
    })

    this.displayCounters()

    const final = (isOk)=>(arg)=>{
      this.testing  = false
      const txt     = isOk ? CONFIG.lang.testsDone.msg : txtFormat.error(String(arg))
      const elapsed = ((Date.now() - start) / 1000).toFixed(1)

      this.terminal.echo(txt)
      this.terminal.echo(txtFormat.info(`(Elapsed time: ${ elapsed }s)`))
    }

    /* Running everything in order: it's actually a bit faster (probably because not queueing again
       and again while waiting in _getIdeData...?). So don't bother with Promise.all anymore...  */
    try{
      for(const conf of confsToRun){
        this.conf = conf
        jsLogger('[TESTING] - start', conf.ide_name)
        if(conf.run_play){
          await this.playFactory(CONFIG.running.testing)()
        }else{
          await this.validateFactory(CONFIG.running.testing)()
        }
        jsLogger('[TESTING] - done', conf.ide_name)
      }
      final(true)()
    }catch{
      final(false)()
    }
  }



  buildCodeGetter(){
    const cbk = this.conf.code ? ()=>this.userContent : ()=>this.corrContent
    if(this.conf.run_play){
      return ()=>this._joinCodeAndPublicSections(cbk())
    }
    return cbk
  }



  async setupRuntimeIDE(){

    if(this.isTesting()){
      this.toSwap = [ await this.getIdeData(this.conf), this.buildCodeGetter() ]
      this.swap()

      // Do NOT clear the scope at the end: would forbid playing with the terminal afterward.
      pyodide.runPython(pyodideFeatureCode('refresher'))
      if(this.conf){
        if(!this.conf.no_clear){
          pyodide.runPython('clear_scope()')
          this._init()
        }
        this.setupFetchers(this.conf)
      }
    }
    return await super.setupRuntimeIDE()
  }



  async teardownRuntimeIDE(runtime){
    try{
      await super.teardownRuntimeIDE(runtime)

    }finally{
      if(!this.isTesting()) return;

      this.swap()               // Has to always occur
      this.teardownFetchers()   // Has to always occur

      const testOutcome = this._analyzeTestOutcome(runtime)
      const success     = !testOutcome
      const classToBe   = !success        ? 'incorrect'
                        : !this.conf.fail ? 'correct'
                                          : ['correct','must-fail']
                                                        // warning: .must-fail always last!
      this.setSvgAndCounters(this.conf, classToBe)
      this.displayCounters()
      this.std_capture.length = 0   // Always...

      if(testOutcome){
        if(!runtime) throw new Error(testOutcome)
        else         console.error(testOutcome)
      }
    }
  }


  _analyzeTestOutcome(runtime){
    if(!runtime) return "Probably failed in the env section..."

    let msg = []

    if(this.conf.in_error_msg && !runtime.stdErr.includes(this.conf.in_error_msg)){
      msg.push(`The error message should contain; "${this.conf.in_error_msg}"`)
    }

    if(this.conf.not_in_error_msg && runtime.stdErr.includes(this.conf.not_in_error_msg)){
      msg.push(`The error message should NOT contain; "${this.conf.not_in_error_msg}"`)
    }

    if(this.conf.std_capture_regex){
      const fullOut = this.std_capture.join('\n')
      if( !this.conf.std_capture_regex.test(fullOut) ){
        msg.push("The std output/error should match " + this.conf.std_capture_regex)
      }
    }

    if(!msg.length && runtime.stopped === this.conf.fail){
      return ""
    }

    msg = [
      `Test failed for ${this.conf.ide_link} :`,
      runtime.stdErr || "No error raised, but...",
      ...msg
    ]
    return msg.join('\n\n')
  }



  /**Setup the pyodide environment so that requests to relative urls are automatically redirected
   * to the correct (original) locations, and setup various sinks to avoids DOM interactions to
   * fail, typically when trying to update img tags through `PyodidePlot` or `mermaid_figure`.
   * */
  setupFetchers(conf){

    CONFIG.relUrlRedirect = `${ CONFIG.baseUrl }/${ conf.rel_dir_url }/`.replace(/[/]{2}/g, '/')

    pyodide.runPython(`

def __hack_pyfetch():
    import re, js
    from functools import wraps
    import pyodide.http as http

    pure_pyfetch = http.pyfetch
    pure_import  = __import__


    @wraps(pure_pyfetch)
    async def pyfetch(url, *a, **kw):
        if isinstance(url,str) and not re.match(r'(https?|ftps?|file)://|www[.]', url):
            url = js.config().relUrlRedirect + url
        return await pure_pyfetch(url, *a, **kw)
    http.pyfetch = pyfetch


    async def fake_fetch(url, *a):
        if isinstance(url,str) and not re.match(r'(https?|ftps?|file)://|www[.]', url):
            url = js.config().relUrlRedirect + url
        return await js.fetch(url, *a)


    class JsMock:

        # ASYNC_CALLS = set('uploaderAsync'.split())

        def __getattr__(self, k):
            if k=='fetch':  return fake_fetch

            # if k in self.ASYNC_CALLS:  return self.async_sink_js

            if self is sink_js or k in ('document',):
                print(k)
                return sink_js
            return getattr(js,k)

        async def async_sink_js(self, *a,**kw):
            return sink_js

        def __call__(self, *a, **kw):
            return sink_js

        def __setattr__(self, k,v):
            setattr(js, k, v)

    fake_js = JsMock()
    sink_js = JsMock()  # HAS to be another instance!

    def fake_import(name, *a, **kw):
        if name == 'js':
            return fake_js
        return pure_import(name, *a, **kw)
    __builtins__.__import__ = fake_import


    def teardown_tests():
        http.pyfetch = pure_pyfetch
        __builtins__.__import__ = pure_import
    __builtins__.teardown_tests = teardown_tests


__hack_pyfetch()
del __hack_pyfetch`)
  }


  teardownFetchers(){
    CONFIG.relUrlRedirect = ''
    pyodide.runPython("teardown_tests()")
  }
}
