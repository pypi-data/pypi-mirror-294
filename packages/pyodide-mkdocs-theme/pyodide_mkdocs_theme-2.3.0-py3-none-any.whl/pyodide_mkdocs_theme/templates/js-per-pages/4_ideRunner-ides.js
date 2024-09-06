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



class _IdeEditorHandler extends TerminalRunner {

  constructor(editorId){
    super(editorId)
    this.termId        = "term_" + editorId
    this.commentIdH    = "#comment_" + editorId
    this.globalIdH     = "#global_" + editorId
    this.inputIdH      = "#input_" + editorId
    this.counterH      = "#compteur_" + editorId
    this.editor        = null
    this.resizedTerm   = true
    this.getCodeToTest = ()=>this.editor.getSession().getValue()
    this._init()
  }

  _init(){
    this.hiddenDivContent = true
  }



  // @Override
  build(){
    const ideThis = this
    if(this.isVert) this.resizedTerm = false

    this.setupAceEditor()   // Create and define this.editor

    // Bind the ### "button":
    $(this.commentIdH).on("click", this.toggleComments.bind(this))

    const ideLoader = txt => {
      this.applyCodeToEditorAndSave(txt)
      this.focusEditor()
    }

    // Bind all buttons below the IDE
    $(this.globalIdH).find("button").each(function(){
      const btn  = $(this)
      const kind = btn.attr('btn_kind')
      let callback
      switch(kind){
        case 'play':      callback = ideThis.playFactory() ; break
        case 'check':     callback = ideThis.validateFactory() ; break

        case 'download':  callback = _=>ideThis.download() ; break
        case 'upload':    callback = _=>uploader(ideLoader) ; break

        case 'restart':   callback = _=>ideThis.restart() ; break
        case 'save':      callback = _=>{ideThis.save(); ideThis.focusEditor()} ; break

        case 'corr_btn':  if(!CONFIG.inServe) return;
                          callback = ideThis.validateCorrFactory() ; break
        case 'show':      if(!CONFIG.inServe) return;
                          callback = ideThis.revealSolutionAndRems.bind(ideThis) ; break

        default: throw new Error(`Y'should never get there, mate... (${ kind })`)
      }
      btn.on('click', callback)
    })


    // Build the related terminal and add the resize listener, because of the intermediate
    // wrapper div, terminals would not resize automatically
    super.build(this.termId)
    window.addEventListener(
      'resize',
      _.throttle( this.handleTerminalWidthTroubles.bind(this), 50, {leading:false, trailing:true} )
    )


    // Then extract its current height and enforce the value on the terminal if isVert is true.
    // This has to be done on "next tick" (not enough anymore => wait... a lot) and after creation
    // of the terminal instance, so that the editor height has been actually applied.
    if(this.isVert){
      // Resize on next tick, once the editor has been filled:
      setTimeout(_=>this.resizeVerticalTerm(false))

      // in case an IDEv is tabbed, it won't scale properly because the editor is not handled
      // the same way, so put in place a "run once" click event, to resize it when the user
      // clicks on the _parent_ div (because the terminal itself is 0px high! XD )
      this.addEventToRunOnce(this.terminal.parent(), 'click', _=>this.resizeVerticalTerm())
    }
  }




  resizeVerticalTerm(mark=true){
    if(!this.isVert || this.resizedTerm) return;
    jsLogger("[CheckPoint] - Handle terminal window size")

    const divHeight = $('#'+this.id).css('height')
    const term_div = $(`${ this.globalIdH } .term_editor_v`)
    term_div.css("height", divHeight)
    this.resizedTerm = mark
  }



  /**Create and setup the ACE editor for the current Ide instance.
   * */
  setupAceEditor() {

    // https://github.com/ajaxorg/ace/blob/092b70c9e35f1b7aeb927925d89cb0264480d409/lib/ace/autocomplete.js#L545
    const options = {
        autoScrollEditorIntoView: false,
        copyWithEmptySelection:   true,               // active alt+flèches pour déplacer une ligne, aussi
        enableBasicAutocompletion:true,
        enableLiveAutocompletion: false,
        enableSnippets:           true,
        tabSize:                  4,
        useSoftTabs:              true,               // 4 spaces instead of tabs
        navigateWithinSoftTabs:   false,              // this is _fucking_ actually "Atomic Soft Tabs"...
        printMargin:              false,              // hide ugly margins...
        maxLines:                 this.maxIdeLines,
        minLines:                 this.minIdeLines,
        mode:                     "ace/mode/python",
        theme:                    getTheme(),
    }

    const editor = this.editor = ace.edit(this.id, options);
    if(CONFIG._devMode) CONFIG.editors[this.id] = editor

    editor.commands.bindKey(
        { win: "Ctrl-Space", mac: "Cmd-Space" }, "startAutocomplete"
    )
    editor.commands.addCommand({
        name: "commentTests",
        bindKey: { win: "Ctrl-I", mac: "Cmd-I" },
        exec: this.toggleComments.bind(this),
    })
    editor.commands.addCommand({
        name: "runPublicTests",
        bindKey: { win: "Ctrl-S", mac: "Cmd-S" },
        exec: this.playFactory(),
    })
    if(this.hasCheckBtn){
        editor.commands.addCommand({
        name: "runValidationTests",
        bindKey: { win: "Ctrl-Enter", mac: "Cmd-Enter" },
        exec: this.validateFactory(),
      })
    }

    // Editor content is saved every 30 keystrokes
    let nChange = 0;
    this.editor.addEventListener("input", _=>{
        if(nChange++ >= CONFIG.ideKeyStrokesSave){
          nChange=0
          this.save()
        }
    })

    // Try to restore a previous session, or extract default starting code:
    let exerciseCode = this.getStartCode(true)
    this.applyCodeToEditorAndSave(exerciseCode)
    this.editor.resize();
  }



  // @Override
  getTerminalBindings(){

    // Ensure the terminal is focused...!
    const asyncTermFocus=(cbk)=>async e=>{
      await cbk(e)
      this.editor.blur()
      this.terminal.focus()
    }
    return ({
      ...super.getTerminalBindings(),
      'CTRL+I': asyncTermFocus(this.toggleComments.bind(this)),    // false for event handling propagation
      'CTRL+S': asyncTermFocus(this.playFactory()),
      ...(this.hasCheckBtn ? {'CTRL+ENTER': asyncTermFocus(this.validateFactory())}:{}),
    })
  }



  /**Automatically gives the focus to the ACE editor with the given id
   * */
  focusEditor(){
    this.editor.focus()
  }


  /**Add the `tests` section to the given code, joining them with the appropriated
   * string/comment if needed.
   * */
  _joinCodeAndPublicSections(userCode){
    const editorCode = [
      userCode,
      this.publicTests
    ].filter(Boolean).join(CONFIG.lang.tests.msg)
    return editorCode
  }



  /**Build (or extract if allowed) the initial code to put in the editor.
   * */
  getStartCode(extractFromLocaleStorage=false){
    let exerciseCode=""

    if(extractFromLocaleStorage){
      exerciseCode = localStorage.getItem(this.id) || ""
    }
    if(!exerciseCode){
      exerciseCode = this._joinCodeAndPublicSections(this.userContent)
    }

    // Enforce at least 2 lines, so that the prompt is always visible for IDEv
    exerciseCode = exerciseCode.replace(/\n+$/,'')
    if(!exerciseCode) exerciseCode = '\n'

    return exerciseCode+"\n"
  }


  /**Takes in the id string of an editor, or an ACE editor as first argument, and the
   * code string to apply to it, and:
   *      - set the editor content to that string
   *      - save the code to the localStorage
   * */
  applyCodeToEditorAndSave(exerciseCode){
    exerciseCode ||= ""
    this.editor.getSession().setValue(exerciseCode);
    this.save(exerciseCode)
  }



  //-------------------------------------------------------------------------



  /**Extract the current content of the given editor, explore it, and toggle all the lines
   * found after the `# Test` token.
   * Rules for toggling or not are:
   *      - leading spaces are ignored.
   *      - comment out if the first character is not "#".
   *      - if the first char is "#" and there is no spaces behind, uncomment.
   * */
  toggleComments(e) {
    if(e && e.preventDefault) e.preventDefault()

    const codeLines = this.getCodeToTest().split('\n')
    const pattern   = CONFIG.lang.tests.as_pattern
    const iTestsToken = codeLines.findIndex(s=>pattern.test(s))

    /// No tests found:
    if(iTestsToken<0) return;

    const toggled = codeLines.slice(iTestsToken+1).map(s=>{
        return s.replace(CONFIG.COMMENTED_PATTERN, (_,spaces,head,tail)=>{
            if(head=='#' && tail!=' ') return spaces+tail
            if(head!='#') return spaces+'#'+head+tail
            return _
        })
    })
    codeLines.splice(iTestsToken+1, toggled.length, ...toggled)
    const repl = codeLines.join('\n')
    this.applyCodeToEditorAndSave(repl)
    this.focusEditor()
  }



  /**Download the current content of the editor to the download folder of the user.
   * */
  download(){           jsLogger("[Download]")

    let ideContent = this.getCodeToTest() + "" // enforce stringification in any case
    downloader(ideContent, this.pyName)
    this.focusEditor()
  }


  /**Reset the content of the editor to its initial content, and reset the localStorage for
   * this editor on the way.
   * */
  restart(){            jsLogger("[Restart]")

    const exerciseCode = this.getStartCode()
    this.applyCodeToEditorAndSave(exerciseCode)
    this.focusEditor()
  }



  /**Save the current IDE content of the user, or the given code, into the localStorage
  * of the navigator.
  * */
  save(givenCode=""){   jsLogger("[Save]")

    const currentCode = givenCode || this.getCodeToTest()
    localStorage.setItem(this.id, currentCode);
  }

  playFactory(){  throw new Error("Should be overridden in child class") }
  validateFactory(){ throw new Error("Should be overridden in child class") }



  isPlaying(){  return this.running == CONFIG.running.play }
  isChecking(){ return this.running == CONFIG.running.validate }
}


















class IdeRunner extends _IdeEditorHandler {



  /**Does nothing, but catch any call on the parent class, which would raise an error
   * because prefillTerm is undefined, for IDEs.
   * */
  prefillTermIfAny(){}



  /**The terminal behaves differently when IDE content is run, so must be handled from here.
   * (mostly: through command lines, the terminal content is not cleared).
   *
   *  - If not paused, the terminal automatically display a new line for a fresh command.
   *  - So clear content only after if got paused.
   *  - Then show to the user that executions started and enforce terminal GUI refresh,
   *    with a tiny pause so that the user has time to see the "cleared" terminal content.
   *  - And relay to super setup methods.
   * */
  async setupRuntimeIDE() {
    jsLogger("[CheckPoint] - setupRuntimeIDE IdeRunner")

    this.resizeVerticalTerm()   // needed in case the first click is on a button
    this.handleTerminalWidthTroubles()

    // save before anything else, in case an error occur somewhere...
    const editorCode = this.getCodeToTest()
    this.save(editorCode)
    this.storeUserCodeInPython('__USER_CODE__', editorCode)

    this.terminal.pause()
    this.terminalDisplayOnStart()
    await sleep(this.delay ?? 200)  // "Blink" terminal, so that the user see a change

    return this.setupRuntime()
  }

  terminalDisplayOnStart(){
    this.terminal.clear()
    this.terminalEcho(CONFIG.lang.runScript.msg)
  }



  async teardownRuntimeIDE(runtime) {
    jsLogger("[CheckPoint] - IdeRunner teardownRuntime")

    // Restore default state first, in case a validation occurred (stdout!)
    runtime.refreshStateWith()

    if(runtime.finalMsg) this.giveFeedback(runtime.finalMsg)

      await this.teardownRuntime(runtime)
      this.storeUserCodeInPython('__USER_CODE__', "")
  }



  /**If successful until now, display the appropriate message in the terminal.
   * */
  codeSnippetEndFeedback(runtime, step){
    if(runtime.stopped || !step) return

    const playing = this.isPlaying()
    const intro   = playing ? "" : CONFIG.lang.validation.msg
    const section = CONFIG.lang[step].msg
    const ok      = CONFIG.lang.successMsg.msg

    let msg = `${ intro }${ section }: ${ ok }`
    if(playing && !this.hasCheckBtn && !this.publicTests){
      msg = CONFIG.lang.successMsgNoTests.msg
    }

    this.terminalEcho(msg)

    // If no error yet and secret tests exist, prepare a "very final" message:
    if(playing && this.hasCheckBtn){
      runtime.finalMsg = CONFIG.lang.unforgettable.msg
    }
  }





  //--------------------------------------------------------------------





  playFactory(runningMan=CONFIG.running.play){
    return this.lockedRunnerWithBigFailWarningFactory(
      runningMan,
      this.setupRuntimeIDE,
      this.playThroughRunner,
      this.teardownRuntimeIDE,
    )
  }

  validateFactory(runningMan=CONFIG.running.validate){
    return this.lockedRunnerWithBigFailWarningFactory(
      runningMan,
      this.setupRuntimeIDE,
      this.validateThroughRunner,
      this.teardownRuntimeIDE,
    )
  }

  validateCorrFactory(){
    const cbk = this.validateFactory()
    const wrapper = async (e)=>{
      jsLogger("[CheckPoint] - corr_btn start")

      const codeGetter   = this.getCodeToTest
      this.getCodeToTest = ()=>this.corrContent
      const profile      = this.profile
      this.data.profile  = null    // REMINDER: getters without setters!

      let out
      try{
        out = await cbk(e)
      }finally{
        jsLogger("[CheckPoint] - corr_btn validation done")
        this.getCodeToTest = codeGetter
        this.data.profile  = profile
      }
      return out
    }
    return wrapper
  }






  //--------------------------------------------------------------------






  async playThroughRunner(runtime){
    await this.runPythonCodeWithOptionsIfNoStdErr(
      this.getCodeToTest(), runtime, CONFIG.section.editor
    )
  }


  /**Return true if the current section allow to decrease the number of attempts,
   * during a validation
   * */
  canDecreaseAttempts(testSection){
    const wanted      = CONFIG.section[ this.decreaseAttemptsOnCodeError ]
    const allowedFrom = CONFIG.sectionOrder[ wanted ]
    const currentAt   = CONFIG.sectionOrder[ testSection ]
    return currentAt >= allowedFrom
  }


  async validateThroughRunner(runtime){

    let decrease_count = this.canDecreaseAttempts(CONFIG.section.editor)

    // If an error, stop everything...
    if(runtime.stopped){
      // ... but decrease the number attempts and run teardown if this was AssertionError.
      if(runtime.isAssertErr){
        this.handleRunOutcome(runtime, decrease_count)
      }

    }else{

      const validation_state = {
        autoLogAssert:    this.autoLogAssert,
        purgeStackTrace:  this.showOnlyAssertionErrorsForSecrets,
        withStdOut:      !this.deactivateStdoutForSecrets,
      }
      const toRun = [
        [this.getCodeToTest(), CONFIG.section.editor,  {}],
        [this.publicTests,     CONFIG.section.public,  validation_state],
        [this.secretTests,     CONFIG.section.secrets, validation_state],
      ]

      for(const [code, testSection, state] of toRun){
        jsLogger("[CheckPoint] - Run validation,", testSection)

        runtime.refreshStateWith(state)
        await this.runPythonCodeWithOptionsIfNoStdErr(code, runtime, testSection)

        if(runtime.stopped){
          decrease_count = this.canDecreaseAttempts(testSection)
          break
        }
      }

      /* Reveal solution and REMs on success, or if the counter reached 0 and the sol&REMs
        content is still encrypted.
        Prepare an appropriate revelation message if needed (`finalMsg`).
      */
      this.handleRunOutcome(runtime, decrease_count)
    }
  }








  //-----------------------------------------------------------------------







  /**Do not forget that all error feedback is already printed to the console. So when it comes to
   * feedback, this method is only there to spot any final message needed.
   * */
  handleRunOutcome(runtime, allowCountDecrease){
    const success    = !runtime.stopped
    const revealable = this.corrRemsMask && this.hiddenDivContent && !this.profile

    jsLogger("[CheckPoint] - handleRunOutcome")
    // jsLogger("[OutCome]", JSON.stringify({ success, revealable, hidden:this.hiddenDivContent, allowCountDecrease: !!allowCountDecrease, mask:this.corrRemsMask, N:this.attemptsLeft}))

    if(!success){
      runtime.finalMsg = ""         // Reset default message "terminé sans erreurs"
      if(allowCountDecrease){
        this.decreaseIdeCounter()
      }
    }

    if( revealable && (success || this.attemptsLeft==0) ){
      jsLogger("[OutCome]", 'reveal!')
      this.buildFinalMessage(runtime, success)
      this.revealSolutionAndRems()

    }else if(success && !revealable && this.corrRemsMask && this.hiddenDivContent){
      runtime.finalMsg = this._buildSuccessMessage()
    }
  }


  /**Decrease the number of tries left, unless:
   *    - The solution is already revealed
   *    - The number of tries is infinite
   *    - There no attempts left (redundant with revelation condition, but hey...)
   */
  decreaseIdeCounter(){
    jsLogger("[CheckPoint] - decreaseIdeCounter")
    if(!this.hiddenDivContent) return    // already revealed => nothing to change.

    // Allow going below 0 so that triggers once only for failure.
    const nAttempts = Math.max(-1, this.attemptsLeft - 1)
    this.data.attempts_left = nAttempts

    // Update the GUI counter if needed (check for encryption in case
    // the user already solved the problem)
    if (Number.isFinite(nAttempts) && nAttempts >= 0){
      $(this.counterH).text(nAttempts)
    }
  }


  /**Given the outcome of the current run, check if the sol&REMs must be revealed or not,
   * and apply the needed DOM modifications if so.
   *
   * Revelation occurs if:
   *    - Sol&REMs are still hidden,
   *    - Some Sol&REMs actually exist,
   *    - The run is successful or all attempts have been consumed.
   *
   * @returns: boolean, telling if the revelation occurred or not.
   */
  revealSolutionAndRems(){
    jsLogger("[CheckPoint] - Enter revealSolutionAndRems")
    const sol_div = $("#solution_" + this.id)

    if(this.hiddenDivContent && this.isEncrypted){
      // Need to check here one more time against hidden_corr because of the show button logic.
      jsLogger("[CheckPoint] - revealed!")
      const compressed = sol_div.text()
      const content = decompressLZW(compressed, "ides.encrypt_corrections_and_rems")
      sol_div.html(content)
      this.hiddenDivContent = false // Forbid coming back here (last in case of errors...)
    }
    sol_div.attr('class', '')       // unhide
    mathJaxUpdate()                 // Enforce formatting, if ever...
  }



  buildFinalMessage(runtime, success){
    jsLogger("[CheckPoint] - buildFinalMessage. Success:", success)
    runtime.finalMsg = success ? this._buildSuccessMessage()
                               : this._getSolRemTxt(false)
  }

  _buildSuccessMessage(){
    const emo = choice(CONFIG.MSG.successEmojis)
    let info = this._getSolRemTxt(true)
    return `${ CONFIG.lang.successHead.msg } ${ emo } ${ CONFIG.lang.successHeadExtra.msg }${ info }`
  }


  _getSolRemTxt(isSuccess){
    if(!this.corrRemsMask) return ""

    const msg=[], sentence=[], mask = this.corrRemsMask

    msg.push( isSuccess ? "\n"+CONFIG.lang.successTail.msg
                        : CONFIG.lang.failHead.msg
    )

    if(mask & 1) sentence.push(CONFIG.lang.revealCorr.msg)
    if(mask===3) sentence.push(CONFIG.lang.revealJoin.msg)
    if(mask & 2) sentence.push(CONFIG.lang.revealRem.msg)

    if(!isSuccess){
        if(sentence.length) sentence[0] = _.capitalize(sentence[0])
        if(mask&2)          sentence.push(CONFIG.lang.failTail.plural)
        else if(mask)       sentence.push(CONFIG.lang.failTail.msg)
    }
    msg.push(...sentence)
    jsLogger("[OutComeSolRemTxt]", JSON.stringify({isSuccess, msg, mask, sentence}))
    return msg.join(' ').trimEnd() + "."
  }
}
